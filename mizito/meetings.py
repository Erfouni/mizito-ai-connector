"""Polls (نظرسنجی) and meeting minutes (صورتجلسه): special messages inside a conversation."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from mizito.app import (
    TEHRAN, WHEN_HELP, AttachmentIds, ConversationId, MessageId, ToolError, UserIds, alarm_options, call, check,
    client, compact, dialog_row, files_in, html_to_text, iso, jalali, load_message, media_attachments,
    minute_summary, parse_when, poll_summary, remember_tasks, send_chat, simplify_message, tool,
)
from mizito_client import MizitoError

# --- polls ---------------------------------------------------------------------------------------


class PollQuestion(BaseModel):
    question: str = Field(description="The question text.")
    options: list[str] = Field(description="2 to 10 answer options.", min_length=2, max_length=10)
    description: str = Field("", description="Optional explanation shown under the question.")
    correct_option: int | None = Field(None, description="Quiz mode only: 0-based index of the correct option.")


def _poll(conversation_id: str, message_id: str) -> dict:
    poll = (load_message(conversation_id, message_id).get("media") or {}).get("polling")
    if not isinstance(poll, dict) or not poll.get("_id"):
        raise ToolError("That message is not a poll (find polls with mizito_get_messages: media_type messageMediaPolling)")
    return poll


@tool("ساخت نظرسنجی", kind="create")
def mizito_create_poll(
    conversation_id: ConversationId,
    questions: Annotated[list[PollQuestion], Field(description="One or more questions, each with its options.", min_length=1)],
    visibility: Annotated[Literal["public", "admins_only", "secret"], Field(description=(
        "public = everyone sees who voted what; admins_only = members see only totals, group admins see each "
        "vote; secret = nobody can see individual votes."))] = "public",
    multiple_answers: Annotated[bool, Field(description="Allow choosing several options per question (not with quiz).")] = False,
    quiz: Annotated[bool, Field(description="Quiz mode: every question needs correct_option; voters see whether they were right.")] = False,
) -> dict:
    """Post a poll (نظرسنجی) in a group or project conversation. Mizito lets only group admins (or admins of
    an advanced project) create polls. Only on the user's explicit request."""
    if quiz and any(q.correct_option is None or not 0 <= q.correct_option < len(q.options) for q in questions):
        raise ToolError("Quiz mode needs a valid correct_option (0-based) for every question")
    polling = {
        "anonymous": visibility != "public",
        "admin_visible": visibility != "secret",
        "multiple_answers": multiple_answers and not quiz,
        "quiz_mode": quiz,
        "multiple_questions": len(questions) > 1,
        "questions": [{
            "subject": q.question,
            "options": [{"text": o} for o in q.options],
            "description": q.description,
            "correct_answer": q.correct_option if quiz else -1,
        } for q in questions],
    }
    message = send_chat(conversation_id, "", {"_": "messageMediaPolling", "polling": polling})
    if not message:
        raise ToolError("The poll was not posted: only group admins (or advanced-project admins) can create polls")
    return {"created": True, "message": simplify_message(message)}


@tool("نتایج نظرسنجی")
def mizito_get_poll_results(conversation_id: ConversationId, message_id: MessageId) -> dict:
    """Results of a poll message: every question with its options, vote counts and percentages, who voted
    for what (only when the poll's visibility lets you see it), your own votes, whether it has ended, and
    Mizito's printable report when the plan provides one."""
    poll = _poll(conversation_id, message_id)
    out = {"poll": poll_summary(poll)}
    try:  # Mizito's printable report (enterprise plans); the counts above come from the poll itself
        out["report"] = html_to_text(client.call("polling.printPollingResults", {"dialog": conversation_id, "polling": poll["_id"]}))
    except MizitoError:
        pass
    return out


@tool("رأی دادن و مدیریت نظرسنجی", kind="update")
def mizito_poll_action(
    conversation_id: ConversationId,
    message_id: Annotated[str, Field(description="Id of the poll message (media_type messageMediaPolling) from mizito_get_messages.")],
    action: Annotated[Literal["vote", "retract_vote", "stop", "save_as_template", "remove_template"], Field(description=(
        "vote = cast your vote (choices); retract_vote = take your vote back; stop = end the poll so nobody can vote "
        "(group admins); save_as_template / remove_template = reuse this poll as a template (admins)."))],
    choices: Annotated[list[list[int]] | None, Field(description=(
        "For vote: one list per question with the 0-based indexes of the chosen options, in question order, "
        "e.g. [[1]] for option 2 of a one-question poll, or [[0], [2, 3]] for two questions."))] = None,
) -> dict:
    """Vote in a poll or manage it. Only on the user's explicit request (a vote is visible to others unless the
    poll is anonymous)."""
    poll = _poll(conversation_id, message_id)
    base = {"dialog": conversation_id, "polling": poll["_id"]}
    if action == "vote":
        if not choices:
            raise ToolError("choices is required for vote")
        questions = poll.get("questions") or []
        votes = {}
        for qi, picked in enumerate(choices):
            if qi >= len(questions):
                raise ToolError(f"The poll has only {len(questions)} question(s)")
            options = questions[qi].get("options") or []
            if len(picked) > 1 and not poll.get("multiple_answers"):
                raise ToolError("This poll allows one answer per question")
            if any(not 0 <= o < len(options) for o in picked):
                raise ToolError(f"Question {qi + 1} has options 0..{len(options) - 1}")
            if picked:
                votes[questions[qi]["_id"]] = [options[o]["_id"] for o in picked]
        check(call("polling.setPollingVote", {**base, "my_votes": votes}), "record the vote")
    elif action == "retract_vote":
        check(call("polling.retractVote", base), "retract the vote")
    elif action == "stop":
        check(call("polling.stopPolling", base, "only group admins can end a poll"), "end the poll")
    else:
        call("polling.setPollingAsTemplate", {**base, "isActive": action == "save_as_template"},
             "templates need admin rights and a plan with templates")
    return {"action": action, "done": True, "poll": poll_summary(_poll(conversation_id, message_id))}


# --- meeting minutes -----------------------------------------------------------------------------


class ActionItem(BaseModel):
    title: str = Field(description="What has to be done (becomes a task).")
    assignee_ids: list[str] = Field(description="Member ids from mizito_list_users responsible for it.")
    deadline: str | None = Field(None, description="Due date. " + WHEN_HELP)
    remind_at: str | None = Field(None, description="Reminder time; puts the task on the calendar. " + WHEN_HELP)
    notes: str = Field("", description="Optional details.")


def _minute_message(conversation_id: str, message_id: str) -> dict:
    message = load_message(conversation_id, message_id)
    media = message.get("media") or {}
    minute = media.get("minute")
    if not isinstance(minute, dict):
        raise ToolError("That message is not meeting minutes (media_type messageMediaMinute)")
    return {"message": message, "minute": minute, "advanced": media.get("_") == "messageMediaMinuteAdvanced"}


def _project_of(conversation_id: str, project_id: str | None) -> str | None:
    return project_id or dialog_row(conversation_id).get("project_entity")


@tool("ثبت صورتجلسه", kind="create")
def mizito_create_minute(
    conversation_id: ConversationId,
    subject: Annotated[str, Field(description="Meeting subject (موضوع جلسه).")],
    date: Annotated[str, Field(description="When the meeting took place. " + WHEN_HELP)],
    location: Annotated[str, Field(description="Where it took place (مکان).")] = "",
    notes: Annotated[str, Field(description="Minutes text: discussion and decisions (plain text, line breaks kept).")] = "",
    action_items: Annotated[list[ActionItem] | None, Field(description="Decisions to follow up (مصوبات); each becomes a task linked to the minutes.")] = None,
    project_id: Annotated[str | None, Field(description="Project for the action-item tasks; defaults to the conversation's project.")] = None,
    attachment_ids: AttachmentIds = None,
    template_id: Annotated[str | None, Field(description="Minute template id from mizito_list_templates(kind='minute') to prefill subject, location and notes.")] = None,
) -> dict:
    """Record meeting minutes (صورتجلسه) in a conversation, the way the web app's «صورتجلسه» button does:
    subject, date/time, place, text and follow-up tasks. Members of the conversation see it as a message and
    get the tasks. Only on the user's explicit request."""
    if template_id:
        template = call("minute.getTemplate", {"template": template_id}) or {}
        subject = subject or template.get("subject") or ""
        location = location or template.get("location") or ""
        notes = notes or html_to_text(template.get("notes"))
    when = parse_when(date)
    tasks = []
    if action_items:
        project = _project_of(conversation_id, project_id)
        if not project:
            raise ToolError("Action items become tasks, which need a project: pass project_id "
                            "(this conversation is not a project conversation)")
        for item in action_items:
            payload = {
                "title": item.title, "notes": item.notes, "assignee": item.assignee_ids, "project": project,
                "kanban_board": None, "labels": [], "attachments": [], "deleted": True,
                "alarm_options": alarm_options(item.remind_at) if item.remind_at else None,
                "progress": 0, "weight": 1, "responsible": None, "checklist": [],
                "from_chat": False, "from_minute": True, "insert_to_chat_group": False,
            }
            if item.deadline:
                payload["deadline"] = iso(item.deadline)
            created = check(client.call("tasks.add", payload), f"create the task {item.title!r}")
            created = [t for t in (created if isinstance(created, list) else [created]) if isinstance(t, dict)]
            remember_tasks(created)
            tasks.extend(created)
    minute = {
        "subject": subject, "location": location,
        "date": iso(date), "time": when.astimezone(TEHRAN).strftime("%H:%M"),
        "notes": notes, "tasks": tasks, "attachments": media_attachments(attachment_ids, wrap=True),
    }
    message = send_chat(conversation_id, "", {"_": "messageMediaMinute", "minute": minute})
    if not message:
        raise ToolError("Mizito did not post the minutes")
    return {"created": True, "message": simplify_message(message)}


@tool("خواندن صورتجلسه")
def mizito_get_minute(
    conversation_id: ConversationId,
    message_id: Annotated[str, Field(description="Id of the minutes message (media_type messageMediaMinute or messageMediaMinuteAdvanced).")],
    with_history: Annotated[bool, Field(description="Also return the edit history of the minutes text.")] = False,
) -> dict:
    """Full meeting minutes: subject, date, place, members, text, follow-up tasks and files. For advanced
    minutes also the state, attendance, comments and sent SMS."""
    found = _minute_message(conversation_id, message_id)
    minute = found["minute"]
    out = {"minute": minute_summary(minute), "advanced": found["advanced"]}
    if found["advanced"] and minute.get("_id"):
        full = client.call("minuteAdvanced.get", {"minuteId": minute["_id"]}) or {}
        out["minute"] = minute_summary(full) or out["minute"]
        out["attendance"] = compact([{"user": client.user_name(m.get("user")), "present": m.get("attendance"),
                                      "comment": m.get("attendance_comments")} for m in full.get("members") or []
                                     if isinstance(m, dict)])
        out["external_members"] = compact(full.get("members_other") or [])
        out["comments"] = compact([{"id": c.get("_id"), "from": client.user_name(c.get("user") or c.get("from")),
                                    "text": html_to_text(c.get("comment")), "date_jalali": jalali(c.get("date")),
                                    "files": files_in(c.get("attachments"))}
                                   for c in client.call("minuteAdvanced.getComments", {"minuteId": minute["_id"]}) or []])
        out["sms_sent"] = compact(client.call("minuteAdvanced.getSmsHistory", {"minuteId": minute["_id"]}) or [])
    elif with_history and minute.get("_id"):
        rows = client.call("minute.history", {"minute_id": minute["_id"]}) or []
        out["history"] = [compact({"by": client.user_name(r.get("user")), "date_jalali": jalali(r.get("date")),
                                   "subject": (r.get("data") or {}).get("subject"),
                                   "notes": html_to_text((r.get("data") or {}).get("notes"))}) for r in rows]
    return compact(out)


@tool("ویرایش صورتجلسه", kind="update")
def mizito_manage_minute(
    conversation_id: ConversationId,
    message_id: Annotated[str, Field(description="Id of the minutes message.")],
    action: Annotated[Literal["edit", "save_as_template", "remove_template"], Field(description=(
        "edit = change subject/date/location/notes (group or workspace admins); save_as_template / remove_template "
        "= reuse these minutes as a template (workspace admins, enterprise plan)."))],
    subject: Annotated[str | None, Field(description="New subject.")] = None,
    date: Annotated[str | None, Field(description="New date/time. " + WHEN_HELP)] = None,
    location: Annotated[str | None, Field(description="New location.")] = None,
    notes: Annotated[str | None, Field(description="New minutes text (replaces the old text).")] = None,
) -> dict:
    """Edit simple meeting minutes or turn them into a template. Advanced minutes are managed with
    mizito_manage_advanced_minute."""
    found = _minute_message(conversation_id, message_id)
    minute = dict(found["minute"])
    if found["advanced"]:
        raise ToolError("These are advanced minutes: use mizito_manage_advanced_minute")
    if action == "edit":
        if all(v is None for v in (subject, date, location, notes)):
            raise ToolError("Nothing to change: pass subject, date, location or notes")
        if subject is not None:
            minute["subject"] = subject
        if location is not None:
            minute["location"] = location
        if notes is not None:
            minute["notes"] = notes
        if date is not None:
            minute["date"] = iso(date)
            minute["time"] = parse_when(date).astimezone(TEHRAN).strftime("%H:%M")
        minute["dialog"] = conversation_id
        call("minute.update", {"dialog": conversation_id, "minute": minute}, "only group admins can edit minutes")
    else:
        call("minute.setMinuteAsTemplate", {"minuteId": minute.get("_id"), "isActive": action == "save_as_template"},
             "templates need workspace admin rights and an enterprise plan")
    return {"action": action, "done": True, "minute": minute_summary(_minute_message(conversation_id, message_id)["minute"])}


# --- advanced minutes (projects with advanced minutes enabled) -----------------------------------

ADVANCED_HINT = "advanced minutes need a project with advanced features (mizito_set_project_advanced) and a plan that includes them"


class ExternalMember(BaseModel):
    name: str = Field(description="Full name of a participant who is not a workspace member.")
    phone: str = Field("", description="Mobile number, for SMS invitations.")


@tool("ثبت صورتجلسه‌ی پیشرفته (دعوت، حضور، امضا)", kind="create")
def mizito_create_advanced_minute(
    conversation_id: Annotated[str, Field(description="Project conversation id (mizito_get_project's conversation_id).")],
    subject: Annotated[str, Field(description="Meeting subject.")],
    date: Annotated[str, Field(description="Meeting date/time. " + WHEN_HELP)],
    location: Annotated[str, Field(description="Meeting place.")],
    member_ids: UserIds,
    agenda: Annotated[str, Field(description="Agenda / notes before the meeting (دستور جلسه).")] = "",
    executive_id: Annotated[str | None, Field(description="Meeting secretary / executive (دبیر جلسه), a member id.")] = None,
    second_executive_id: Annotated[str | None, Field(description="Second executive, a member id.")] = None,
    observer_id: Annotated[str | None, Field(description="Observer (ناظر), a member id.")] = None,
    external_members: Annotated[list[ExternalMember] | None, Field(description="Participants outside the workspace.")] = None,
    reminder_hours_before: Annotated[int, Field(description="Remind members this many hours before; 0 = no reminder.", ge=0, le=168)] = 3,
) -> dict:
    """Create advanced meeting minutes (صورتجلسه‌ی پیشرفته) as a draft in a project conversation. The flow is:
    create (draft) -> mizito_manage_advanced_minute send_invitations -> after the meeting write the text with
    update -> send_for_signature -> members sign. Requires advanced minutes on the project."""
    project = dialog_row(conversation_id).get("project_entity")
    if not project:
        raise ToolError("Advanced minutes live in a project conversation (mizito_get_project's conversation_id)")
    when = parse_when(date)
    minute = {
        "subject": subject, "location": location, "date": iso(date), "time": when.astimezone(TEHRAN).strftime("%H:%M"),
        "notes_pre": agenda, "member_owner": client.my_user_id(), "member_executive": executive_id,
        "member_executive2": second_executive_id, "member_observer": observer_id,
        "members": [{"user": u} for u in member_ids],
        "members_other": [m.model_dump() for m in external_members or []],
        "notes": "", "tasks": [], "has_reminder": reminder_hours_before > 0,
        "reminder_hours_before": reminder_hours_before or 3, "project": project, "state": 0,
    }
    message = send_chat(conversation_id, "", {"_": "messageMediaMinuteAdvanced", "minute": minute})
    if not message:
        raise ToolError("Mizito did not create the advanced minutes: " + ADVANCED_HINT)
    return {"created": True, "message": simplify_message(message)}


@tool("مدیریت صورتجلسه‌ی پیشرفته", kind="update")
def mizito_manage_advanced_minute(
    conversation_id: ConversationId,
    message_id: Annotated[str, Field(description="Id of the advanced minutes message (media_type messageMediaMinuteAdvanced).")],
    action: Annotated[Literal["update", "send_invitations", "send_for_signature", "sign", "comment", "edit_comment",
                              "delete_comment", "send_sms", "save_as_template", "remove_template"], Field(description=(
        "update = change subject/date/location/agenda/notes; send_invitations = invite members (state draft -> "
        "invited, SMS to members); send_for_signature = send the final text and decisions for signing; sign = sign "
        "(sign_message_id = the signature request message you received); comment / edit_comment / delete_comment; "
        "send_sms = SMS to members with sms_template; save_as_template / remove_template."))],
    subject: Annotated[str | None, Field(description="For update: new subject.")] = None,
    date: Annotated[str | None, Field(description="For update: new date/time. " + WHEN_HELP)] = None,
    location: Annotated[str | None, Field(description="For update: new place.")] = None,
    agenda: Annotated[str | None, Field(description="For update: new agenda.")] = None,
    notes: Annotated[str | None, Field(description="For update: the minutes text / decisions (متن صورتجلسه).")] = None,
    text: Annotated[str | None, Field(description="For comment / edit_comment: the comment text.")] = None,
    comment_id: Annotated[str | None, Field(description="For edit_comment / delete_comment: comment id from mizito_get_minute.")] = None,
    sign_message_id: Annotated[str | None, Field(description="For sign: id of the signature request message (media_type messageMediaMinuteForSign).")] = None,
    sms_template: Annotated[Literal["cancel", "send-for-sign", "time-changed", "location-changed",
                                    "time-location-changed", "check-tasks"] | None, Field(description=(
        "For send_sms: cancel = meeting cancelled; send-for-sign = please sign; time-changed / location-changed / "
        "time-location-changed; check-tasks = reminder to finish the decisions' tasks."))] = None,
) -> dict:
    """Run the advanced-minutes workflow. Only on the user's explicit request (invitations and SMS reach every
    member)."""
    found = _minute_message(conversation_id, message_id)
    minute_id = found["minute"].get("_id")
    if not found["advanced"] or not minute_id:
        raise ToolError("That message is not advanced minutes; use mizito_manage_minute")
    project = found["minute"].get("project") or dialog_row(conversation_id).get("project_entity")
    where = {"minuteId": minute_id, "dialog": conversation_id, "project": project}
    if action == "update":
        minute = call("minuteAdvanced.get", {"minuteId": minute_id}, ADVANCED_HINT) or {}
        for key, value in (("subject", subject), ("location", location), ("notes_pre", agenda), ("notes", notes)):
            if value is not None:
                minute[key] = value
        if date is not None:
            minute["date"] = iso(date)
            minute["time"] = parse_when(date).astimezone(TEHRAN).strftime("%H:%M")
        call("minuteAdvanced.update", {"minute": minute, "dialog": conversation_id, "project": project}, ADVANCED_HINT)
    elif action == "send_invitations":
        check(call("minuteAdvanced.sendDraft", where, ADVANCED_HINT), "send the invitations")
    elif action == "send_for_signature":
        check(call("minuteAdvanced.sendForSign", where, ADVANCED_HINT), "send the minutes for signature")
    elif action == "sign":
        if not sign_message_id:
            raise ToolError("sign_message_id is required for sign")
        call("minuteAdvanced.sign", {"mid": sign_message_id, "dialog": conversation_id, "minuteId": minute_id}, ADVANCED_HINT)
    elif action in ("comment", "edit_comment", "delete_comment"):
        if action != "delete_comment" and not text:
            raise ToolError("text is required")
        if action != "comment" and not comment_id:
            raise ToolError("comment_id is required")
        if action == "comment":
            call("minuteAdvanced.newComment", {"minuteId": minute_id, "comment": text, "attachments": []}, ADVANCED_HINT)
        elif action == "edit_comment":
            check(call("minuteAdvanced.editComment", {"minuteId": minute_id, "commentId": comment_id, "newComment": text}),
                  "edit the comment (others may have seen it)")
        else:
            check(call("minuteAdvanced.deleteComment", {"minuteId": minute_id, "commentId": comment_id}),
                  "delete the comment (others may have seen it)")
    elif action == "send_sms":
        if not sms_template:
            raise ToolError("sms_template is required for send_sms")
        call("minuteAdvanced.sendSms", {**where, "template": sms_template}, ADVANCED_HINT)
    else:
        call("minuteAdvanced.setMinuteAsTemplate", {"minuteId": minute_id, "isActive": action == "save_as_template"},
             "templates need an enterprise plan")
    return {"action": action, "done": True, "minute": mizito_get_minute(conversation_id, message_id)["minute"]}


# --- templates -----------------------------------------------------------------------------------


@tool("الگوها (صورتجلسه، نظرسنجی، وظیفه)")
def mizito_list_templates(
    kind: Annotated[Literal["minute", "advanced_minute", "poll", "task"], Field(description="Which templates to list.")],
    project_id: Annotated[str | None, Field(description="Required for kind='task': the project whose task templates to list.")] = None,
) -> dict:
    """Saved templates (الگو): minute and poll templates of the workspace, or the task templates of a project
    (advanced projects). Use a minute template with mizito_create_minute(template_id=...) and a task template
    with mizito_create_task(template_id=...)."""
    if kind == "task":
        if not project_id:
            raise ToolError("project_id is required for task templates")
        rows = call("taskTemplates.getAllTemplates", {"projectId": project_id},
                    "task templates need a project with advanced features and a plan that includes them") or []
    else:
        endpoint = {"minute": "minute.getTemplates", "advanced_minute": "minuteAdvanced.getTemplates",
                    "poll": "polling.getTemplates"}[kind]
        rows = call(endpoint, {}) or []
    return {"kind": kind, "count": len(rows), "templates": compact(rows)}

"""Tasks (وظایف): listing, details, creation, editing, reminders and repeats, comments, boards, templates,
and the calendar (تقویم), which shows tasks at their reminder time."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated, Literal

from pydantic import Field

from mizito.app import (
    REPEAT_HELP, TEHRAN, WHEN_HELP, AttachmentIds, LabelIds, ProjectId, TaskId, ToolError, alarm_options, call, check, client, compact, files_in, html_text, html_to_text, iso, jalali, load_task,
    media_attachments, names, now_jalali, project_full, remember_tasks, save_task, task_ref, task_token, tool,
)
from mizito_client import MizitoError

Weekdays = Annotated[list[Literal["sat", "sun", "mon", "tue", "wed", "thu", "fri"]] | None, Field(
    description="For weekly: the weekdays to repeat on; for monthly_first/last_weekday: exactly one weekday.")]
DayOfMonth = Annotated[int | Literal["first", "last"] | None, Field(
    description="For monthly / every_2_months / every_3_months: day of the Jalali month (1-31), first or last.")]
RepeatUntil = Annotated[str | None, Field(description="Stop repeating after this date. " + WHEN_HELP)]
RepeatTimes = Annotated[int | None, Field(description="Stop after this many repetitions (instead of repeat_until).", ge=1, le=1000)]
Repeat = Annotated[Literal[
    "none", "daily", "every_other_day", "even_days", "odd_days", "weekly", "every_2_weeks", "every_3_weeks",
    "monthly", "every_2_months", "every_3_months", "monthly_first_weekday", "monthly_last_weekday", "yearly",
], Field(description=REPEAT_HELP)]


# --- reading -------------------------------------------------------------------------------------


@tool("فهرست وظایف")
def mizito_list_tasks(
    scope: Annotated[Literal["mine", "following", "project", "done"], Field(description=(
        'mine = open tasks assigned to me (کارهای من); following = open tasks I assigned to others or follow '
        '(پیگیری از دیگران); project = open tasks of project_id; done = completed tasks, newest first (انجام شده).'))] = "mine",
    project_id: Annotated[str | None, Field(description="Required when scope='project'.")] = None,
    offset: Annotated[int, Field(description="Skip this many tasks (paging).", ge=0)] = 0,
) -> dict:
    """Tasks (وظایف) with their ids, titles, assignees, project, board, dates and progress. Use a task's
    `_id` as task_id in every other task tool."""
    if scope == "project":
        if not project_id:
            raise ToolError("project_id is required when scope='project'")
        payload = {"project_id": project_id, "all": True, "sort_type": "default", "filter": None}
    elif scope == "done":
        payload = {"done_timeline": True, "filter": {}}
    else:
        payload = {"inbox" if scope == "mine" else "outbox": True, "sort_type": "default", "filter": None}
    payload["from"] = offset
    raw = client.call("tasks.upcoming", payload) or []
    remember_tasks(raw)
    data = compact(raw)
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                row["assignee_names"] = names(row.get("assignee"))
                for key in ("alarm_at", "deadline", "deadline_start"):
                    if row.get(key):
                        row[f"{key}_jalali"] = jalali(row[key])
        return {"scope": scope, "offset": offset, "count": len(data), "tasks": data}
    return {"scope": scope, "offset": offset, **data}


@tool("جزئیات یک وظیفه")
def mizito_get_task(task_id: TaskId) -> dict:
    """Full details of one task: description, assignees, approvers, project and board, start/deadline/reminder
    (with Jalali dates), repeat rule, checklist (item ids for mizito_check_task_item), labels, progress and
    attached files (file_id for mizito_read_file)."""
    raw = load_task(task_id)
    task = compact({k: v for k, v in raw.items() if k != "attachments"})
    if isinstance(task.get("notes"), str):
        task["notes"] = html_to_text(task["notes"])
    task["assignee_names"] = names(raw.get("assignee"))
    task["approver_names"] = names(raw.get("responsible"))
    task["owner_name"] = client.user_name(raw.get("owner"))
    for key in ("alarm_at", "deadline", "deadline_start", "created_at", "completed_at"):
        if raw.get(key):
            task[f"{key}_jalali"] = jalali(raw[key])
    task["files"] = files_in(raw.get("attachments"))
    return compact(task)


@tool("گزارش‌های (کامنت‌های) وظیفه")
def mizito_get_task_comments(task_id: TaskId) -> dict:
    """Comments / progress reports (گزارش) on a task, oldest first, with author, date, replies, mentions and
    attached files."""
    rows = client.call("tasks.getComments", {"token": task_token(task_id)}) or []
    comments = [compact({
        "id": r.get("_id"),
        "from": client.user_name(r.get("comment_owner")),
        "date": r.get("comment_at"),
        "date_jalali": jalali(r.get("comment_at")),
        "text": html_to_text(r.get("comment")),
        "reply_to": r.get("replied_comment_id"),
        "mentions": names(r.get("mention")),
        "files": files_in(r.get("attachments")),
        "edited": r.get("edited") or None,
        "deleted": r.get("deleted") or None,
    }) for r in rows if isinstance(r, dict)]
    return {"task_id": task_id, "count": len(comments), "comments": comments}


@tool("سابقه، بازدید و امکانات پیشرفته‌ی وظیفه")
def mizito_get_task_extras(task_id: TaskId) -> dict:
    """Extra information about a task: who created and who has seen it (and when), its Gantt placement and
    dependencies, automation buttons you can press (mizito_run_task_automation), its workflow step and custom
    field history. Advanced-project parts are omitted when the project does not use them."""
    task = load_task(task_id)
    token = task["access_token"]
    out: dict = {"task": task_ref(task)}
    seen = client.call("tasks.getSeenDetails", {"token": token}) or {}
    created = seen.get("created") or {}
    out["created_by"] = client.user_name(created.get("owner"))
    out["created_jalali"] = jalali(created.get("created_at"))
    out["first_seen"] = [{"user": client.user_name(r.get("user")), "date_jalali": jalali(r.get("date"))}
                         for r in seen.get("first_user_seen") or [] if isinstance(r, dict)]
    out["last_seen"] = [{"user": client.user_name(r.get("user")), "date_jalali": jalali(r.get("date"))}
                        for r in seen.get("last_user_seen") or [] if isinstance(r, dict)]
    workflow = "formRequestTemplate.getTaskWorkflow" if task.get("is_form_request") else "projectAutomationWorkflow.getTaskWorkflow"
    optional = (
        ("gantt", "tasks.ganttGetTaskInfo", {"project": task.get("project"), "token": token}),
        ("automation_buttons", "projectAutomation.getTaskAutomateButtons", {"token": token}),
        ("workflow", workflow, {"token": token}),
        ("custom_field_history", "projectAutomation.customParam.getValuesHistory", {"token": token}),
    )
    for key, endpoint, payload in optional:  # parts of advanced projects; absent elsewhere
        try:
            value = compact(client.call(endpoint, payload))
        except MizitoError:
            continue
        if value:
            out[key] = value
    return compact(out)


@tool("تقویم من یا پروژه")
def mizito_calendar(
    year: Annotated[int | None, Field(description="Jalali year, e.g. 1405. Defaults to the current year in Tehran.")] = None,
    month: Annotated[int | None, Field(description="Jalali month 1-12 (1 = Farvardin ... 7 = Mehr ... 12 = Esfand). Defaults to the current month.", ge=1, le=12)] = None,
    by: Annotated[Literal["reminder", "deadline"], Field(description="reminder = the calendar's normal view (tasks at their reminder time); deadline = tasks by due date (advanced projects).")] = "reminder",
    project_id: Annotated[str | None, Field(description="Show this project's calendar (every member's tasks) instead of your own.")] = None,
) -> dict:
    """Tasks on the Mizito calendar (تقویم) for one Jalali month. The calendar places tasks by their reminder
    time, so a task with only a deadline is not on it. Repeating tasks and tasks without a time are returned
    separately. Check it before adding events to avoid duplicates."""
    if not year or not month:
        year, month, _ = now_jalali()
    base = {"project_id": project_id} if project_id else {"inbox": True}
    base.update({"all": True, "from": None})
    visibility = "alarm_at" if by == "reminder" else "deadline"
    scheduled = client.call("tasks.upcoming", {**base, "filter": {
        "calendar_year": year, "calendar_month": month, "visibility_type": visibility}}) or []
    unscheduled = client.call("tasks.upcoming", {**base, "filter": {"calendar_repeated_and_without_time": True}}) or []
    remember_tasks(scheduled)
    remember_tasks(unscheduled)
    return {
        "year": year, "month": month, "by": by, "project_id": project_id, "count": len(scheduled),
        "tasks": [task_ref(t) for t in scheduled],
        "repeating_or_without_time": [task_ref(t) for t in unscheduled],
    }


@tool("سابقه‌ی تغییرات وظیفه یا پروژه")
def mizito_get_history(
    kind: Annotated[Literal["task", "project"], Field(description="What item the id belongs to.")],
    item_id: Annotated[str, Field(description="Task id or project id.")],
) -> dict:
    """Change history (سابقه تغییرات) of a task or project: who changed what, and when."""
    if kind == "task":
        task = load_task(item_id)
        rows = client.call("tasks.history", {"token": task["access_token"], "tid": task["_id"]}) or []
    else:
        rows = client.call("projects.history", {"project_id": item_id}) or []
    for row in rows:
        if isinstance(row, dict):
            if isinstance(row.get("user"), str):
                row["user_name"] = client.user_name(row["user"])
            if row.get("date"):
                row["date_jalali"] = jalali(row["date"])
    return {"kind": kind, "id": item_id, "count": len(rows), "history": compact(rows)}


# --- creating and editing ------------------------------------------------------------------------


def _template(project_id: str, template_id: str) -> dict:
    for tpl in call("taskTemplates.getAllTemplates", {"projectId": project_id},
                    "task templates need an advanced project and a plan that includes them") or []:
        if tpl.get("_id") == template_id:
            return tpl
    raise ToolError(f"Task template {template_id!r} not found in this project (mizito_list_templates)")


@tool("ساخت وظیفه", kind="create")
def mizito_create_task(
    title: Annotated[str, Field(description="Task title.")],
    assignee_ids: Annotated[list[str], Field(description="Who does it: member ids from mizito_list_users (mizito_whoami's user_id for yourself).")],
    project_id: Annotated[str, Field(description="Project the task belongs to (Mizito requires one), from mizito_list_projects.")],
    notes: Annotated[str, Field(description="Description (plain text).")] = "",
    deadline: Annotated[str | None, Field(description="Due date (مهلت); does NOT put the task on the calendar. " + WHEN_HELP)] = None,
    checklist: Annotated[list[str] | None, Field(description="Checklist item titles.")] = None,
    remind_at: Annotated[str | None, Field(description="Reminder / scheduled time (زمان یادآوری): puts the task on the calendar and notifies the assignees. " + WHEN_HELP)] = None,
    start: Annotated[str | None, Field(description="Start date (تاریخ شروع), used by the Gantt chart. " + WHEN_HELP)] = None,
    board_id: Annotated[str | None, Field(description="Kanban board (column) id from mizito_get_project; default = the first board.")] = None,
    label_ids: LabelIds = None,
    approver_ids: Annotated[list[str] | None, Field(description="With several assignees: who gives the final approval (تأییدکننده نهایی); must be among the assignees.")] = None,
    repeat: Repeat = "none",
    repeat_weekdays: Weekdays = None,
    repeat_day_of_month: DayOfMonth = None,
    repeat_until: RepeatUntil = None,
    repeat_times: RepeatTimes = None,
    weight: Annotated[int | None, Field(description="Task weight, for advanced projects with weighted progress.", ge=1, le=1000)] = None,
    attachment_ids: AttachmentIds = None,
    template_id: Annotated[str | None, Field(description="Start from a task template of the project (mizito_list_templates kind='task'); explicit arguments win.")] = None,
    post_to_project_chat: Annotated[bool, Field(description="Also announce the task in the project conversation, like the web form's default.")] = False,
    one_copy_per_assignee: Annotated[bool, Field(description="Create a separate copy of the task for each assignee (enterprise plans).")] = False,
) -> dict:
    """Create a task (وظیفه) in a project, with everything the web form offers: assignees, description,
    start / deadline / reminder, repetition, checklist, board, labels, approvers, weight, files and
    templates. Remember: only remind_at places a task on the calendar. Only on the user's explicit request."""
    full = project_full(project_id)
    if template_id:
        tpl = _template(project_id, template_id)
        notes = notes or tpl.get("notes") or ""
        assignee_ids = assignee_ids or [a for a in tpl.get("assignee_default") or [] if a]
        checklist = checklist if checklist is not None else [c.get("title") for c in tpl.get("checklist_default") or []]
        label_ids = label_ids if label_ids is not None else tpl.get("labels_default")
        board_id = board_id or tpl.get("kanban_board_default")
        weight = weight or tpl.get("weight_default")
        approver_ids = approver_ids or tpl.get("responsible_default") or None
        if not remind_at and isinstance(tpl.get("default_due"), int):
            day = datetime.now(TEHRAN) + timedelta(days=tpl["default_due"])
            remind_at = day.replace(hour=8, minute=0, second=0, microsecond=0).isoformat()
    if not assignee_ids:
        raise ToolError("assignee_ids is required")
    if approver_ids and (len(assignee_ids) < 2 or any(a not in assignee_ids for a in approver_ids)):
        raise ToolError("approver_ids only apply to tasks with several assignees and must be among them")
    if repeat != "none" and not remind_at:
        raise ToolError("A repeating task needs remind_at (the time of the first occurrence)")
    # Same fields and defaults as the web client's new-task form; it sends no deadline key when there is none.
    payload = {
        "title": title, "notes": notes, "assignee": assignee_ids, "project": project_id,
        "kanban_board": board_id, "labels": label_ids or [], "attachments": media_attachments(attachment_ids, wrap=True),
        "deleted": False,
        "alarm_options": alarm_options(remind_at, repeat, repeat_weekdays, repeat_day_of_month, repeat_until,
                                       repeat_times) if remind_at else None,
        "progress": 0, "weight": weight or 1, "responsible": approver_ids or None,
        "checklist": [{"checked": False, "title": item} for item in checklist or []],
        "from_chat": False, "from_minute": False,
        "insert_to_chat_group": bool(post_to_project_chat and full.get("dialog")),
    }
    if deadline:
        payload["deadline"] = iso(deadline)
    if start:
        payload["deadline_start"] = iso(start)
    if template_id:
        payload["from_template"] = template_id
    if one_copy_per_assignee:
        payload.update(copy_users=assignee_ids, assignee=None)
    result = client.call("tasks.add", payload)
    if result is False:
        raise ToolError("Mizito rejected the task (check project_id and that the assignees are project members)")
    check(result, "create the task")
    tasks = [t for t in (result if isinstance(result, list) else [result]) if isinstance(t, dict)]
    remember_tasks(tasks)
    if remind_at:
        for t in tasks:  # older servers ignore alarm_options on add; set the reminder the way the calendar does
            if not t.get("alarm_at") and repeat == "none":
                client.call("tasks.snooze", {"token": t["access_token"], "project": t.get("project"),
                                             "alarm_at": iso(remind_at), "update_repeat_base": False})
        tasks = [load_task(t["_id"]) for t in tasks]
    out = {"created": len(tasks), "tasks": [task_ref(t) for t in tasks]}
    if deadline and not remind_at:
        out["note"] = "No remind_at: the task is listed under 'without time' on the calendar."
    return out


@tool("افزودن رویداد به تقویم", kind="create")
def mizito_create_calendar_event(
    project_id: Annotated[str, Field(description="Project to hold the event (its members can see it).")],
    title: Annotated[str, Field(description="Event title.")],
    start: Annotated[str, Field(description="Start time; the event appears on the calendar here. " + WHEN_HELP)],
    end: Annotated[str | None, Field(description="End time (stored as the task deadline). " + WHEN_HELP)] = None,
    description: Annotated[str, Field(description="Details.")] = "",
    attendee_ids: Annotated[list[str] | None, Field(description="Participants (member ids); default = you.")] = None,
    repeat: Repeat = "none",
    repeat_weekdays: Weekdays = None,
) -> dict:
    """Add an event to the Mizito calendar. Mizito has no separate event object: the calendar shows tasks at
    their reminder time, so this creates a task with reminder = start and deadline = end, assigned to the
    attendees. Check mizito_calendar(project_id=...) first to avoid duplicates."""
    return mizito_create_task(title=title, assignee_ids=attendee_ids or [client.my_user_id()], project_id=project_id,
                              notes=description, deadline=end, remind_at=start, repeat=repeat, repeat_weekdays=repeat_weekdays)


def _editable(task_id: str) -> dict:
    task = load_task(task_id)
    if task.get("completed"):
        raise ToolError("Mizito does not let you edit a completed task: reopen it first (mizito_set_task_completed)")
    return task


@tool("ویرایش وظیفه", kind="update")
def mizito_update_task(
    task_id: TaskId,
    title: Annotated[str | None, Field(description="New title.")] = None,
    notes: Annotated[str | None, Field(description="New description (plain text; replaces the old one).")] = None,
    assignee_ids: Annotated[list[str] | None, Field(description="New assignee list (replaces the current one).")] = None,
    label_ids: Annotated[list[str] | None, Field(description="New label list (replaces the current one), ids from mizito_list_labels.")] = None,
    project_id: Annotated[str | None, Field(description="Move the task to this project (it lands on that project's first board).")] = None,
    board_id: Annotated[str | None, Field(description="Move to this board of the task's project (or use mizito_move_task_to_board).")] = None,
    start: Annotated[str | None, Field(description='New start date, or "" to clear it. ' + WHEN_HELP)] = None,
    deadline: Annotated[str | None, Field(description='New deadline, or "" to clear it. ' + WHEN_HELP)] = None,
    approver_ids: Annotated[list[str] | None, Field(description="Final approvers among the assignees; [] removes approval.")] = None,
    weight: Annotated[int | None, Field(description="Task weight (advanced projects).", ge=1, le=1000)] = None,
    add_checklist_items: Annotated[list[str] | None, Field(description="Checklist items to append.")] = None,
    add_attachment_ids: AttachmentIds = None,
) -> dict:
    """Edit a task's fields; omitted fields stay as they are. Moving to another project needs membership there.
    Completed tasks cannot be edited (reopen first). For the reminder use mizito_set_task_reminder, for
    repetition mizito_set_task_repeat, for progress mizito_set_task_progress."""
    changes: dict = {}
    for key, value in (("title", title), ("notes", notes), ("assignee", assignee_ids), ("labels", label_ids), ("weight", weight)):
        if value is not None:
            changes[key] = value
    if project_id is not None:
        changes.update(project=project_id, kanban_board=None)
    if board_id is not None:
        changes["kanban_board"] = board_id
    if start is not None:
        changes["deadline_start"] = iso(start) if start else None
    if deadline is not None:
        changes["deadline"] = iso(deadline) if deadline else None
    if approver_ids is not None:
        changes["responsible"] = approver_ids or None
    if not changes and not add_checklist_items and not add_attachment_ids:
        raise ToolError("Nothing to change")
    task = _editable(task_id)
    if add_checklist_items:
        changes["checklist"] = list(task.get("checklist") or []) + [{"checked": False, "title": t} for t in add_checklist_items]
    if add_attachment_ids:
        changes["attachments"] = list(task.get("attachments") or []) + media_attachments(add_attachment_ids, wrap=True)
    save_task(task, **changes)
    after = load_task(task_id)
    if project_id is not None and after.get("project") != project_id:
        raise ToolError("Mizito did not move the task (are you a member of the target project?)")
    return {"updated": True, "task": task_ref(after)}


@tool("ثبت گزارش (کامنت) روی وظیفه", kind="create")
def mizito_comment_on_task(
    task_id: TaskId,
    text: Annotated[str, Field(description="Comment / progress report text (plain text).")],
    reply_to_comment_id: Annotated[str | None, Field(description="Answer this comment (id from mizito_get_task_comments).")] = None,
    mention_user_ids: Annotated[list[str] | None, Field(description="Members to notify (enterprise plans).")] = None,
    attachment_ids: AttachmentIds = None,
) -> dict:
    """Add a comment / progress report (گزارش) to a task; everyone on the task sees it. Works for tasks
    created from request forms too."""
    task = load_task(task_id)
    token = task["access_token"]
    payload = {"token": token, "comment": html_text(text), "attachments": media_attachments(attachment_ids, wrap=True),
               "mention": mention_user_ids or [], "reply_id": reply_to_comment_id}
    client.call("formRequestTemplate.newComment" if task.get("is_form_request") else "tasks.newComment", payload)
    comments = client.call("tasks.getComments", {"token": token}) or []
    return {"commented": True, "comments_count": len(comments) if isinstance(comments, list) else None}


@tool("ویرایش یا حذف گزارش وظیفه", kind="update")
def mizito_manage_task_comment(
    task_id: TaskId,
    comment_id: Annotated[str, Field(description="Comment id from mizito_get_task_comments.")],
    action: Annotated[Literal["edit", "delete"], Field(description="edit = replace the text; delete = remove it.")],
    text: Annotated[str | None, Field(description="New text, for edit.")] = None,
) -> dict:
    """Edit or delete one of your own task comments. Mizito refuses once other people have seen it."""
    token = task_token(task_id)
    if action == "edit":
        if not text:
            raise ToolError("text is required for edit")
        result = client.call("tasks.editComment", {"token": token, "commentId": comment_id, "newComment": text})
    else:
        result = client.call("tasks.deleteComment", {"token": token, "commentId": comment_id})
    if not result:
        raise ToolError("Mizito refused: the comment was already seen by others, or it is not yours")
    return {"task_id": task_id, "comment_id": comment_id, "action": action, "done": True}


@tool("انجام شد / بازگشایی وظیفه", kind="set")
def mizito_set_task_completed(
    task_id: TaskId,
    completed: Annotated[bool, Field(description="true = mark done, false = reopen.")] = True,
) -> dict:
    """Mark a task done (انجام شد) or reopen it. In projects with approval, the approver finishes it."""
    task = load_task(task_id)
    client.call("tasks.setCompleted", {"token": task["access_token"], "completed": completed, "project": task.get("project")})
    return {"task": task_ref(load_task(task_id))}


@tool("تعیین مهلت وظیفه", kind="set")
def mizito_set_task_deadline(
    task_id: TaskId,
    deadline: Annotated[str | None, Field(description="New deadline, or null to clear it. " + WHEN_HELP)],
) -> dict:
    """Set or clear a task's deadline (مهلت). This does not put it on the calendar: use
    mizito_set_task_reminder for that."""
    task = load_task(task_id)
    client.call("tasks.updateDeadline", {"token": task["access_token"], "project": task.get("project"), "deadline": iso(deadline)})
    return {"task": task_ref(load_task(task_id))}


@tool("درصد پیشرفت وظیفه", kind="set")
def mizito_set_task_progress(
    task_id: TaskId,
    progress: Annotated[int, Field(description="Progress percentage 0-100.", ge=0, le=100)],
) -> dict:
    """Set a task's progress percentage (درصد پیشرفت)."""
    client.call("tasks.updateProgress", {"token": task_token(task_id), "progress": progress})
    return {"task": task_ref(load_task(task_id))}


@tool("زمان یادآوری وظیفه (تقویم)", kind="set")
def mizito_set_task_reminder(
    task_id: TaskId,
    remind_at: Annotated[str | None, Field(description="Reminder time, or null to remove it. " + WHEN_HELP)],
) -> dict:
    """Put a task on the calendar at a reminder time (زمان یادآوری), move it, or remove the reminder. The
    assignees are notified at that time. Completed tasks cannot get reminders."""
    task = load_task(task_id)
    client.call("tasks.snooze", {"token": task["access_token"], "project": task.get("project"),
                                 "alarm_at": iso(remind_at), "update_repeat_base": False})
    after = load_task(task_id)
    if remind_at and not after.get("alarm_at"):
        raise ToolError("Mizito did not set the reminder" + (
            ": the task is completed, reopen it first" if after.get("completed") else ""))
    return {"task": task_ref(after)}


@tool("تکرار وظیفه", kind="set")
def mizito_set_task_repeat(
    task_id: TaskId,
    repeat: Repeat,
    first_at: Annotated[str | None, Field(description="Time of the first/next occurrence; defaults to the task's current reminder. " + WHEN_HELP)] = None,
    weekdays: Weekdays = None,
    day_of_month: DayOfMonth = None,
    until: RepeatUntil = None,
    times: RepeatTimes = None,
) -> dict:
    """Make a task repeat (تکرار وظیفه): daily, weekly on chosen days, monthly on a day, yearly and more,
    optionally until a date or for a number of times. repeat='none' stops repeating. Every occurrence appears
    on the calendar."""
    task = _editable(task_id)
    when = first_at or task.get("alarm_at") or (task.get("alarm_options") or {}).get("date")
    if not when:
        raise ToolError("The task has no reminder yet: pass first_at")
    options = alarm_options(when, repeat, weekdays, day_of_month, until, times)
    save_task(task, alarm_options=options)
    after = load_task(task_id)
    return {"task": task_ref(after), "repeat": compact(after.get("alarm_options"))}


@tool("تیک زدن آیتم چک‌لیست", kind="set")
def mizito_check_task_item(
    task_id: TaskId,
    item_id: Annotated[str, Field(description="Checklist item `_id` from mizito_get_task's checklist.")],
    checked: Annotated[bool, Field(description="true = tick, false = untick.")] = True,
) -> dict:
    """Tick (or untick) one checklist item of a task."""
    client.call("tasks.setChecklistCheckedValue", {"token": task_token(task_id), "checklistId": item_id, "checked": checked})
    task = load_task(task_id)
    return {"checklist": compact([{"id": i.get("_id"), "title": i.get("title"), "checked": i.get("checked")}
                                  for i in task.get("checklist") or []])}


@tool("جابه‌جایی وظیفه بین ستون‌های کانبان", kind="set")
def mizito_move_task_to_board(
    task_id: TaskId,
    board_id: Annotated[str, Field(description="Target board id from mizito_get_project's boards (same project).")],
    position: Annotated[Literal["top", "bottom"], Field(description="Put the task at the top or bottom of the board.")] = "bottom",
) -> dict:
    """Move a task to another kanban board (column) of its project, like dragging it in the web app's
    kanban view (e.g. from «برای انجام» to «در حال انجام»)."""
    task = load_task(task_id)
    project_id = task.get("project")
    boards = [b.get("_id") for b in project_full(project_id).get("kanban_boards") or []]
    if board_id not in boards:
        raise ToolError("That board is not in the task's project (see mizito_get_project)")
    rows = client.call("tasks.upcoming", {"project_id": project_id, "all": True, "sort_type": "default",
                                          "filter": None, "from": 0}) or []
    remember_tasks(rows)
    first_board = boards[0] if boards else None
    weights = [r.get("kanban_weight") or 0 for r in rows
               if r.get("_id") != task_id and (r.get("kanban_board") or first_board) == board_id]
    if not weights:
        weight = 1000
    elif position == "bottom":
        weight = max(weights) + 100
    else:
        weight = min(weights) / 2
    call("tasks.setKanbanWeight", {"token": task["access_token"], "projectId": project_id,
                                   "kanbanBoardId": board_id, "kanbanWeight": weight},
         "moving tasks may need project membership or admin rights")
    after = load_task(task_id)
    return {"moved": after.get("kanban_board") == board_id or (board_id == first_board and not after.get("kanban_board")),
            "task": task_ref(after)}


@tool("نشان، حذف، بازگردانی، لینک اشتراک وظیفه", kind="update")
def mizito_manage_task(
    task_id: TaskId,
    action: Annotated[Literal["bookmark", "unbookmark", "delete", "restore", "unfollow", "remove_from_board",
                              "create_share_link"], Field(description=(
        "bookmark/unbookmark (نشان‌شده‌ها); delete = move to trash (restore can undo it); restore; unfollow = stop "
        "following a task you assigned (پیگیری); remove_from_board = project admin removes it from the board in "
        "approval projects; create_share_link = a link that shows the task to people outside the workspace."))],
) -> dict:
    """Bookmark, delete, restore, unfollow or share a task."""
    token = task_token(task_id)
    result: dict = {"task_id": task_id, "action": action, "done": True}
    if action in ("bookmark", "unbookmark"):
        client.call("tasks.toggleBookmark", {"token": token, "bookmarked": action == "bookmark"})
    elif action == "delete":
        client.call("tasks.removeTask", {"token": token})
    elif action == "restore":
        client.call("tasks.removeTaskUndo", {"token": token})
    elif action == "unfollow":
        client.call("tasks.removeFromTracking", {"token": token})
    elif action == "remove_from_board":
        task = load_task(task_id)
        call("tasks.removeFromBoard", {"token": token, "project_id": task.get("project")},
             "only project admins of approval (advanced) projects can do this")
    else:
        from mizito.files import safe_link

        result["share_link"] = safe_link(call("tasks.createShareLink", {"token": token}, "sharing may need an enterprise plan"))
    return result


# --- task templates ------------------------------------------------------------------------------


@tool("مدیریت الگوی وظیفه‌ی پروژه", kind="update")
def mizito_manage_task_template(
    project_id: ProjectId,
    action: Annotated[Literal["create", "update", "delete"], Field(description="Create a new template, change one, or delete one.")],
    template_id: Annotated[str | None, Field(description="For update/delete: id from mizito_list_templates(kind='task').")] = None,
    title: Annotated[str | None, Field(description="Template name / default task title.")] = None,
    notes: Annotated[str | None, Field(description="Default description.")] = None,
    assignee_ids: Annotated[list[str] | None, Field(description="Default assignees.")] = None,
    checklist: Annotated[list[str] | None, Field(description="Default checklist items.")] = None,
    label_ids: LabelIds = None,
    board_id: Annotated[str | None, Field(description="Default board.")] = None,
    reminder_after_days: Annotated[int | None, Field(description="Default reminder: this many days after the task is created.", ge=0, le=365)] = None,
    weight: Annotated[int | None, Field(description="Default weight.", ge=1, le=1000)] = None,
    active: Annotated[bool | None, Field(description="Whether members can use the template.")] = None,
) -> dict:
    """Create, edit or delete a project's task template (الگوی وظیفه), used to create similar tasks quickly.
    Needs an advanced project and a plan with templates."""
    hint = "task templates need an advanced project, project admin rights and a plan that includes them"
    if action == "delete":
        if not template_id:
            raise ToolError("template_id is required for delete")
        call("taskTemplates.remove", {"projectId": project_id, "templateId": template_id}, hint)
        return {"deleted": True, "template_id": template_id}
    if action == "update":
        if not template_id:
            raise ToolError("template_id is required for update")
        template = dict(_template(project_id, template_id))
    else:
        if not title:
            raise ToolError("title is required for create")
        template = {"title": "", "notes": "", "assignee_default": [None], "responsible_default": [], "default_due": None,
                    "checklist_default": [], "attachments_default": [], "labels_default": [], "weight_default": None,
                    "kanban_board_default": None, "is_active": True}
    for key, value in (("title", title), ("notes", notes), ("labels_default", label_ids), ("kanban_board_default", board_id),
                       ("default_due", reminder_after_days), ("weight_default", weight), ("is_active", active)):
        if value is not None:
            template[key] = value
    if assignee_ids is not None:
        template["assignee_default"] = assignee_ids or [None]
    if checklist is not None:
        template["checklist_default"] = [{"title": c} for c in checklist]
    template["projectId"] = project_id
    endpoint = "taskTemplates.save" if action == "update" else "taskTemplates.add"
    result = call(endpoint, {"projectId": project_id, "template": template}, hint)
    return {"saved": True, "template": compact(result if isinstance(result, dict) else template)}

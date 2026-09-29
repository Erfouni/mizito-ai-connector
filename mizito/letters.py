"""Letters (نامه‌ها / کارتابل): threaded internal mail, referrals (پاراف) and the secretariat (دبیرخانه)."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mizito.app import (
    WHEN_HELP, AttachmentIds, Confirm, LabelIds, ThreadId, ToolError, UserIds, call, check, client, compact,
    files_in, html_text, html_to_text, iso, jalali, letter_people, media_attachments, names, now_iso,
    require_confirm, tool,
)
from mizito_client import MizitoError


def _row(item: dict) -> dict:
    return compact({
        "id": item.get("_id"),
        "thread": item.get("thread"),
        "subject": item.get("subject"),
        "from": client.user_name(item.get("from")),
        "to": names(letter_people(item)) or None,
        "date": item.get("send_date"),
        "date_jalali": jalali(item.get("send_date")),
        "unread": item.get("unread"),
        "messages_in_thread": item.get("count"),
        "attachments": item.get("attachments_count"),
        "letter_number": item.get("sec_number") or item.get("sec_num"),
        "preview": html_to_text(item.get("short_content") or item.get("raw_content")),
    })


@tool("فهرست و جستجوی نامه‌ها")
def mizito_list_letters(
    box: Annotated[Literal["inbox", "outbox", "archived"], Field(description="inbox = received, outbox = sent (and your referrals), archived = archived received letters.")] = "inbox",
    offset: Annotated[int, Field(description="Skip this many letters (paging).", ge=0)] = 0,
    search: Annotated[str | None, Field(description="Search words in subject and text (switches to search mode across boxes).")] = None,
    read_status: Annotated[Literal["any", "unread", "read"], Field(description="Filter by read state (search mode).")] = "any",
    attachments: Annotated[Literal["any", "with", "without"], Field(description="Filter by attachments (search mode).")] = "any",
    from_user_id: Annotated[str | None, Field(description="Only letters from this member (search mode).")] = None,
    to_user_id: Annotated[str | None, Field(description="Only letters to this member (search mode).")] = None,
    label_id: Annotated[str | None, Field(description="Only letters with this label (mizito_list_labels kind='inbox').")] = None,
    conversation_id: Annotated[str | None, Field(description="Only letters linked to this conversation / customer file.")] = None,
    secretariat: Annotated[Literal["any", "incoming", "outgoing"], Field(description="Only registered official letters: incoming (وارده) or outgoing (صادره).")] = "any",
    letter_number: Annotated[str | None, Field(description="Official letter number (شماره نامه) to find.")] = None,
) -> dict:
    """Letters (نامه‌ها، کارتابل), newest first. Without filters it lists a box; any filter switches to Mizito's
    search, which looks across boxes. Use `thread` with mizito_get_letter_thread, mizito_reply_letter and
    mizito_manage_letter."""
    filtered = any([search, read_status != "any", attachments != "any", from_user_id, to_user_id, conversation_id,
                    secretariat != "any", letter_number])
    if filtered or label_id:
        status = {"any": 0, "read": 1, "unread": 2}
        payload = {
            "mode": "search", "offset": offset, "from": from_user_id, "to": to_user_id,
            "read_unread_status": status[read_status], "has_attach_status": {"any": 0, "without": 1, "with": 2}[attachments],
            "search_str": search or "", "labels": [], "dialog": conversation_id, "date_range": None,
            "only_secretariat": secretariat != "any" or bool(letter_number),
            "secretariat_letter_type": {"any": 0, "incoming": 1, "outgoing": 2}[secretariat],
            "secretariat_register_from": None, "secretariat_register_to": None, "secretariat_sec_num": letter_number,
        }
        if not filtered:  # a label alone is the web app's label view
            payload = {"mode": "search", "offset": offset}
        if label_id:
            payload["label_id"] = label_id
    else:
        payload = {"mode": box, "offset": offset}
        if box == "outbox":
            payload["outbox_mode"] = "all"
    letters = client.call("inbox.getInbox", payload) or []
    items = [_row(item) for item in letters]
    return {"box": "search" if filtered or label_id else box, "offset": offset, "count": len(items), "letters": items}


@tool("خواندن کامل یک رشته نامه")
def mizito_get_letter_thread(
    thread_id: ThreadId,
    with_seen_details: Annotated[bool, Field(description="Also say who has read each letter and when.")] = False,
) -> dict:
    """Every letter of a thread with full text: the first letter, then its replies and referrals (پاراف) in
    order, with sender, recipients, dates, files (file_id for mizito_read_file), labels and linked
    conversations."""
    root = client.call("inbox.getHistory", {"thread": thread_id}) or {}
    if not isinstance(root, dict) or not root.get("_id"):
        raise ToolError(f"Letter thread {thread_id!r} not found")
    letters = []
    for letter in [root, *(root.get("messages") or [])]:
        row = compact({
            "id": letter.get("_id"),
            "from": client.user_name(letter.get("from")),
            "to": names(letter_people(letter)),
            "date": letter.get("send_date"),
            "date_jalali": jalali(letter.get("send_date")),
            "subject": letter.get("subject"),
            "content": html_to_text(letter.get("content")),
            "reply_to": letter.get("reply_to"),
            "files": files_in(letter.get("attachments")),
        })
        if with_seen_details and letter.get("_id"):
            try:
                seen = client.call("inbox.getSeenDetails", {"thread": thread_id, "msgId": letter["_id"]}) or {}
                rows = seen.get("to") if isinstance(seen, dict) else seen
                row["seen"] = [compact({"user": client.user_name(s.get("user") or s.get("user_id")),
                                        "seen_jalali": jalali(s.get("seen_date") or s.get("date")),
                                        "unread": not (s.get("seen_date") or s.get("date")) or None})
                               for s in rows or [] if isinstance(s, dict)]
            except MizitoError:
                pass
        letters.append(row)
    out = {"thread": thread_id, "subject": root.get("subject"), "count": len(letters), "letters": letters}
    for key, endpoint in (("labels", "inbox.getMessageLabels"), ("linked_conversations", "inbox.getMessageDialogs")):
        try:
            value = client.call(endpoint, {"thread": thread_id})
            if value:
                out[key] = compact(value)
        except MizitoError:
            pass
    return out


# --- write tools ---------------------------------------------------------------------------------


@tool("ارسال نامه‌ی جدید", kind="create")
def mizito_send_letter(
    to_user_ids: UserIds,
    subject: Annotated[str, Field(description="Subject (موضوع).")],
    content: Annotated[str, Field(description="Letter text (plain text; line breaks kept).")],
    attachment_ids: AttachmentIds = None,
    label_ids: LabelIds = None,
) -> dict:
    """Send a new letter (نامه) to workspace members. Only on the user's explicit request, with recipients,
    subject and text confirmed."""
    payload = {"to": to_user_ids, "subject": subject, "content": html_text(content),
               "attachments": media_attachments(attachment_ids, wrap=False), "tasks_insert_to_chat_groups": [],
               "labels": label_ids or []}
    return {"sent": True, "result": compact(check(client.call("inbox.send", payload), "send the letter"))}


@tool("پاسخ یا پاراف (ارجاع) نامه", kind="create")
def mizito_reply_letter(
    thread_id: ThreadId,
    content: Annotated[str, Field(description="Reply / referral text.")],
    to_user_ids: Annotated[list[str] | None, Field(description="Recipients. Default: everyone on the last letter (reply). Other people = a referral (پاراف / ارجاع) of the thread to them.")] = None,
    attachment_ids: AttachmentIds = None,
) -> dict:
    """Reply inside a letter thread, or refer (پاراف) the thread to other members by choosing to_user_ids.
    Only on the user's explicit request."""
    root = client.call("inbox.getHistory", {"thread": thread_id}) or {}
    if not isinstance(root, dict) or not root.get("_id"):
        raise ToolError(f"Letter thread {thread_id!r} not found")
    me = client.my_user_id()
    last = ([root, *(root.get("messages") or [])])[-1]
    if to_user_ids:
        recipients = to_user_ids
    else:
        people = {last.get("from"), *letter_people(last)}
        recipients = sorted(p for p in people if p and p != me) or [me]  # a thread with yourself
    payload = {"to": recipients, "subject": "", "content": html_text(content),
               "attachments": media_attachments(attachment_ids, wrap=False), "tasks_insert_to_chat_groups": [],
               "labels": [], "reply_to": last.get("_id"), "thread": thread_id}
    return {"sent": True, "to": names(recipients), "result": compact(check(client.call("inbox.send", payload), "send the reply"))}


@tool("مدیریت نامه (آرشیو، نشان، برچسب، اتصال، حذف)", kind="update")
def mizito_manage_letter(
    thread_id: ThreadId,
    action: Annotated[Literal["archive", "unarchive", "bookmark", "unbookmark", "mark_read", "set_labels",
                              "link_conversations", "delete_letter", "delete_thread"], Field(description=(
        "archive / unarchive (box says whether it is in your inbox or outbox); bookmark / unbookmark; mark_read; "
        "set_labels (label_ids replace the current ones); link_conversations = attach the thread to conversations or "
        "customer files (conversation_ids); delete_letter = delete one of your referrals (letter_id); delete_thread = "
        "delete the whole letter with all referrals and files. Deleting is irreversible and needs confirm = subject."))],
    box: Annotated[Literal["inbox", "outbox"], Field(description="For archive/unarchive: which side of the thread.")] = "inbox",
    label_ids: LabelIds = None,
    conversation_ids: Annotated[list[str] | None, Field(description="For link_conversations: the full list of conversation ids.")] = None,
    letter_id: Annotated[str | None, Field(description="For delete_letter: the letter (referral) id from mizito_get_letter_thread.")] = None,
    confirm: Confirm = None,
) -> dict:
    """Archive, bookmark, label, link or delete a letter thread."""
    where = {"thread": thread_id}
    if action in ("archive", "unarchive"):
        endpoint = "inbox." + ("archive" if action == "archive" else "unArchive") + (".sender" if box == "outbox" else "")
        client.call(endpoint, where)
    elif action in ("bookmark", "unbookmark"):
        client.call("inbox.toggleBookmark", {**where, "bookmarked": action == "bookmark"})
    elif action == "mark_read":
        client.call("inbox.seen", where)
    elif action == "set_labels":
        client.call("inbox.changeMessageLabels", {**where, "labels": label_ids or []})
    elif action == "link_conversations":
        client.call("inbox.changeMessageDialogs", {**where, "dialogs": conversation_ids or []})
    else:
        root = client.call("inbox.getHistory", where) or {}
        require_confirm(confirm, root.get("subject"), "letter")
        if action == "delete_letter":
            if not letter_id:
                raise ToolError("letter_id is required for delete_letter")
            mid, whole = letter_id, False
        else:
            mid, whole = root.get("_id"), True
        result = client.call("inbox.deleteMessage", {"mid": mid, "isDeleteThread": whole})
        if not isinstance(result, dict) or not result.get("ok"):
            raise ToolError(f"Mizito did not delete it: {(result or {}).get('errorMessage') if isinstance(result, dict) else result}")
    return {"thread": thread_id, "action": action, "done": True}


@tool("ثبت شماره‌ی نامه در دبیرخانه", kind="update")
def mizito_register_letter(
    thread_id: ThreadId,
    direction: Annotated[Literal["incoming", "outgoing"], Field(description="incoming = نامه وارده (from outside), outgoing = نامه صادره.")],
    register_date: Annotated[str | None, Field(description="Registration date. " + WHEN_HELP)] = None,
    external_number: Annotated[str | None, Field(description="For incoming letters: the sender's letter number (required).")] = None,
    external_date: Annotated[str | None, Field(description="For incoming letters: the sender's letter date (required). " + WHEN_HELP)] = None,
    custom_number: Annotated[str | None, Field(description="Use this secretariat number instead of the next automatic one.")] = None,
) -> dict:
    """Register a letter in the secretariat (دبیرخانه) and give it an official number. Needs secretariat
    access in a plan that includes it."""
    hint = "the secretariat needs a plan that includes it and secretariat access"
    options = dict(call("inbox.getLastSecretariatStatus", {}, hint) or {})
    options["type"] = 1 if direction == "incoming" else 2
    options["sec_register_date"] = iso(register_date) if register_date else options.get("sec_register_date") or now_iso()
    if direction == "incoming":
        if not external_number or not external_date:
            raise ToolError("Incoming letters need external_number and external_date")
        options["inbox_message_in_number"] = external_number
        options["inbox_message_in_date"] = iso(external_date)
    options["custom_number"] = custom_number or options.get("next_sec_number")
    endpoint = "inbox.registerInLetter" if direction == "incoming" else "inbox.registerOutLetter"
    result = check(call(endpoint, {"thread": thread_id, "letterOptions": options}, hint), "register the letter")
    return {"registered": True, "result": compact(result)}


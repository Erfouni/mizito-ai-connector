"""Chat: conversations, messages, groups."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from mizito.app import (
    AttachmentIds, Confirm, ConversationId, MessageId, ToolError, UserId, UserIds, call, chat_full, client,
    compact, dialog_row, html_text, iso, jalali, load_message, media_attachments, messages_count, parse_when,
    require_confirm, send_chat, simplify_message, tool,
)
from mizito_client import MizitoError

PAGE_SIZE = 15  # chat.getHistory always returns 15 messages per offset step


@tool("فهرست گفتگوها")
def mizito_list_conversations(
    unread_only: Annotated[bool, Field(description="Only conversations with unread messages.")] = False,
    kind: Annotated[Literal["all", "private", "group", "customer"], Field(
        description="private = one-to-one chats, group = groups, channels and project conversations, customer = CRM customer files.")] = "all",
    limit: Annotated[int, Field(description="Maximum rows to return (newest activity first).", ge=1, le=1000)] = 100,
) -> dict:
    """Chat conversations (گفتگوها) of the workspace, newest activity first, with unread and message counts
    and whether they are pinned. Use the ids with mizito_get_messages, mizito_send_message and the other chat
    tools."""
    data = client.call("chat.getDialogs", {}) or {}
    pinned = {p if isinstance(p, str) else p.get("_id") for p in data.get("pin_dialogs") or []}
    out = []
    for d in data.get("dialogs", []):
        if unread_only and not d.get("unread_count"):
            continue
        d_kind = "group" if d.get("is_group") else "customer" if d.get("is_customer_entity") else "private"
        if kind != "all" and d_kind != kind:
            continue
        out.append(compact({
            "id": d["_id"],
            "title": client.dialog_title(d),
            "type": d_kind,
            "project_id": d.get("project_entity"),
            "unread": d.get("unread_count", 0),
            "messages_count": d.get("messages_count"),
            "last_message_date": d.get("last_message_date"),
            "last_message_jalali": jalali(d.get("last_message_date")),
            "pinned": d["_id"] in pinned,
        }))
    out.sort(key=lambda x: x.get("last_message_date") or "", reverse=True)
    return {"total": len(out), "conversations": out[:limit]}


@tool("خواندن پیام‌های یک گفتگو")
def mizito_get_messages(
    conversation_id: ConversationId,
    count: Annotated[int, Field(description="How many messages to return (max 600).", ge=1, le=600)] = 50,
    offset: Annotated[int, Field(description="How many of the newest messages to skip (0 = latest). Use the returned next_offset to read further back.", ge=0)] = 0,
    from_date: Annotated[str | None, Field(description=(
        "Instead of offset: return the messages sent from this date/time onwards (ISO or Jalali, e.g. 1405/07/01 or "
        "1405/07/01 14:00); continue forward with the returned newer_offset as offset."))] = None,
) -> dict:
    """Messages of one conversation, oldest-to-newest within the returned window, with sender, text, files
    (file_id for mizito_read_file), tasks, polls, meeting minutes and replies. Reading does not mark anything as
    seen. Page backwards with next_offset, or jump to a date with from_date."""
    total = messages_count(conversation_id)
    want, index, start = count, 0, None
    if from_date:
        start = parse_when(from_date, default_time=(0, 0))
        mid = call("chat.getMessageByDate", {"dialog": conversation_id, "date": iso(from_date, default_time=(0, 0))})
        if not mid:
            return {"conversation_id": conversation_id, "messages_count": total, "returned": 0, "messages": [],
                    "note": "No message on or after that date"}
        index = (client.call("chat.getMessageIndex", {"dialog": conversation_id, "mid": mid}) or {}).get("msg_index") or total
        index = _first_index_since(conversation_id, total, index, start)  # Mizito finds the date only by day
        want = count + PAGE_SIZE
        offset = max(0, total - index - want + 1)
    messages: dict[str, dict] = {}
    cursor = offset
    while len(messages) < want:
        batch = client.call("chat.getHistory", {"dialog": conversation_id, "offset": cursor}) or []
        for m in batch:
            messages.setdefault(m.get("_id"), m)
        cursor += PAGE_SIZE
        if len(batch) < PAGE_SIZE:
            break
    ordered = sorted(messages.values(), key=lambda m: m.get("msg_index") or 0)
    if start:
        ordered = [m for m in ordered if (m.get("msg_index") or 0) >= index and _sent_after(m, start)][:count]
        last = ordered[-1].get("msg_index") if ordered else total
        return {
            "conversation_id": conversation_id, "messages_count": total, "returned": len(ordered),
            "newer_offset": max(0, total - last - count) if last < total else None,
            "messages": [simplify_message(m) for m in ordered],
        }
    ordered = ordered[-count:]
    next_offset = offset + len(ordered)
    return {
        "conversation_id": conversation_id,
        "messages_count": total,
        "returned": len(ordered),
        "next_offset": next_offset if not total or next_offset < total else None,
        "messages": [simplify_message(m) for m in ordered],
    }


def _sent_after(message: dict, start: datetime) -> bool:
    try:
        return datetime.fromisoformat(str(message.get("date")).replace("Z", "+00:00")) >= start
    except ValueError:
        return True


def _first_index_since(conversation_id: str, total: int, low: int, start: datetime) -> int:
    """Binary search (one history page per step) for the first message index sent at/after `start`,
    beginning at `low`, the first message of that day according to Mizito."""
    high = total
    while high - low > PAGE_SIZE:
        middle = (low + high) // 2
        page = client.call("chat.getHistory", {"dialog": conversation_id, "offset": total - middle}) or []
        newest = max(page, key=lambda m: m.get("msg_index") or 0, default=None)
        if newest is None:
            break
        if _sent_after(newest, start):
            high = newest.get("msg_index") or middle
        else:
            low = (newest.get("msg_index") or middle) + 1
    return low


@tool("جستجو در پیام‌ها")
def mizito_search_messages(
    query: Annotated[str, Field(description="Words to search for (Persian or English).")],
    scope: Annotated[Literal["chat", "customers"], Field(description="chat = all conversations, customers = CRM customer files.")] = "chat",
    offset: Annotated[int, Field(description="Skip this many results (page with offset + count).", ge=0)] = 0,
) -> dict:
    """Full-text search across every chat message of the workspace (or customer conversations), newest
    first, with the conversation each hit belongs to. Tip: Mizito text may use Arabic ي/ك instead of Persian
    ی/ک; search both spellings when a name is not found."""
    results = client.call("chat.search", {"mode": scope, "search_str": query, "offset": offset}) or []
    out = []
    for m in results:
        item = simplify_message(m)
        chat = m.get("chat_full") or {}
        item["conversation_id"] = m.get("dialog")
        item["conversation_title"] = chat.get("title") or None
        sender = m.get("from_user") or {}
        if sender:
            item["from"] = " ".join(p for p in (sender.get("first_name"), sender.get("last_name")) if p)
        out.append(compact(item))
    return {"query": query, "offset": offset, "count": len(out), "results": out}


@tool("جزئیات یک پیام (چه کسی دیده)")
def mizito_get_message_info(conversation_id: ConversationId, message_id: MessageId) -> dict:
    """Who has seen a message and when, plus whether you can still edit or delete it (Mizito only allows
    editing before the other side has seen it). Also returns the message itself."""
    message = simplify_message(load_message(conversation_id, message_id))
    details = call("chat.getStatusDetails", {"dialog": conversation_id, "mid": message_id}) or {}
    return compact({
        "message": message,
        "seen_by": [{"user": client.user_name(r.get("user_id")), "date": r.get("date"), "date_jalali": jalali(r.get("date"))}
                    for r in details.get("users_seen") or [] if isinstance(r, dict)],
        "can_edit": details.get("can_update"),
        "can_delete": details.get("can_delete"),
        "can_delete_as_admin": details.get("can_delete_admin_"),
    })


# --- write tools ---------------------------------------------------------------------------------


@tool("ارسال پیام", kind="create")
def mizito_send_message(
    conversation_id: ConversationId,
    text: Annotated[str, Field(description="Message text (plain text; line breaks are kept). May be empty when sending files.")],
    reply_to_message_id: Annotated[str | None, Field(description="Message id to reply to (from mizito_get_messages).")] = None,
    attachment_ids: AttachmentIds = None,
) -> dict:
    """Send a chat message as the logged-in user. For someone you have no chat with yet, first get the
    conversation with mizito_start_conversation. Files: upload with mizito_upload_file and pass their ids; each
    file goes as its own message and the text is sent with the last file. Only on the user's explicit request,
    with recipient and wording confirmed."""
    files = media_attachments(attachment_ids, wrap=False)
    if not text and not files:
        raise ToolError("Nothing to send: give text and/or attachment_ids")
    sent = []
    for i, media in enumerate(files):
        caption = text if i == len(files) - 1 else ""
        sent.append(send_chat(conversation_id, caption, media, reply_to_message_id if i == 0 else None))
    if not files:
        sent.append(send_chat(conversation_id, text, None, reply_to_message_id))
    found = [simplify_message(m) for m in sent if m]
    out = {"sent": True, "conversation_id": conversation_id, "messages": found}
    if len(found) < len(sent):
        out["note"] = "Mizito accepted the message but it was not in the latest history yet."
    return out


@tool("شروع گفتگوی خصوصی", kind="create")
def mizito_start_conversation(user_id: UserId) -> dict:
    """Get (or create) the private conversation with a workspace member, to send them messages."""
    for d in (client.call("chat.getDialogs", {}) or {}).get("dialogs", []):
        if d.get("peer_user") == user_id and not d.get("is_group"):
            return {"conversation_id": d["_id"], "title": client.dialog_title(d), "created": False}
    dialog = client.call("chat.createDialog", {"user": user_id}) or {}
    return {"conversation_id": dialog.get("_id"), "title": client.user_name(user_id), "created": True}


@tool("علامت خوانده‌شده برای گفتگو", kind="set")
def mizito_mark_conversation_read(conversation_id: ConversationId) -> dict:
    """Mark every message of a conversation as seen. Mizito sends read receipts to the other members."""
    count = messages_count(conversation_id)
    client.call("chat.seen", {"dialog": conversation_id, "seen_count": count})
    return {"conversation_id": conversation_id, "seen_count": count}


@tool("مدیریت یک پیام (ویرایش، حذف، سنجاق، نشان)", kind="update")
def mizito_manage_message(
    conversation_id: ConversationId,
    message_id: MessageId,
    action: Annotated[Literal["edit", "delete", "delete_as_admin", "pin", "unpin", "bookmark", "unbookmark",
                              "mark_mention_unread", "remove_mention"], Field(description=(
        "edit = replace the text of your own message (only before others saw it); delete = delete your own message "
        "for everyone; delete_as_admin = a group admin deletes someone else's message; pin/unpin = pin at the top of "
        "the conversation; bookmark/unbookmark = your saved messages (نشان‌شده‌ها); mark_mention_unread / "
        "remove_mention = for mention notices in the Mizito bot conversation."))],
    text: Annotated[str | None, Field(description="New text, required for edit.")] = None,
) -> dict:
    """Act on one message. Message ids come from mizito_get_messages. Deleting cannot be undone."""
    dialog = {"dialog": conversation_id}
    if action == "edit":
        if not text:
            raise ToolError("text is required for edit")
        details = client.call("chat.getStatusDetails", {**dialog, "mid": message_id}) or {}
        if details and not details.get("can_update"):
            raise ToolError("Mizito only lets you edit your own message before the other side has seen it")
        client.call("chat.updateSentMessage", {**dialog, "mid": message_id, "newMessage": html_text(text)})
    elif action in ("delete", "delete_as_admin"):
        endpoint = "chat.removeSentMessage" if action == "delete" else "chat.removeSentMessageAdmin"
        call(endpoint, {**dialog, "mid": message_id}, "only your own messages, or group admins for others' messages")
    elif action in ("pin", "unpin"):
        endpoint = "chat.addPinMessage" if action == "pin" else "chat.removePinMessage"
        call(endpoint, {**dialog, "message": message_id}, "pinning needs group admin rights")
    elif action in ("bookmark", "unbookmark"):
        client.call("chat.toggleBookmark", {**dialog, "mid": message_id, "bookmarked": action == "bookmark"})
    elif action == "mark_mention_unread":
        call("chat.convertMentionToUnProcessed", {**dialog, "mid": message_id})
    else:
        call("chat.removeMentionMessage", {**dialog, "mid": message_id})
    return {"conversation_id": conversation_id, "message_id": message_id, "action": action, "done": True}


@tool("مدیریت گفتگو/گروه", kind="update")
def mizito_manage_conversation(
    conversation_id: ConversationId,
    action: Annotated[Literal["pin", "unpin", "mute", "unmute", "rename", "add_member", "remove_member",
                              "make_admin", "remove_admin", "make_private", "remove_photo", "delete"], Field(description=(
        "pin/unpin in your conversation list; mute/unmute notifications; rename a group (title); add_member / "
        "remove_member / make_admin / remove_admin (user_id; needs group admin rights); make_private turns a public "
        "group or channel into a normal one; remove_photo; delete removes the whole group for everyone "
        "(irreversible, needs confirm = the group's title; project conversations are archived with "
        "mizito_archive_project instead)."))],
    title: Annotated[str | None, Field(description="New title, for rename.")] = None,
    user_id: Annotated[str | None, Field(description="Member id from mizito_list_users, for member actions.")] = None,
    confirm: Confirm = None,
) -> dict:
    """Manage a conversation or group (گروه). Member changes are announced in the group by Mizito."""
    dialog = {"dialog": conversation_id}
    if action in ("pin", "unpin"):
        client.call("chat.pinDialog" if action == "pin" else "chat.unpinDialog", dialog)
    elif action in ("mute", "unmute"):
        client.call("chat.saveSettings", {**dialog, "mute": action == "mute"})
    elif action == "rename":
        if not title:
            raise ToolError("title is required for rename")
        call("chat.updateTitle", {**dialog, "title": title}, "only group admins can rename")
    elif action in ("add_member", "remove_member", "make_admin", "remove_admin"):
        if not user_id:
            raise ToolError(f"user_id is required for {action}")
        if action == "add_member":
            call("chat.inviteUser", {**dialog, "user": user_id}, "only group admins can add members")
        elif action == "remove_member":
            call("chat.deleteUser", {**dialog, "user": user_id}, "only group admins can remove members")
        else:
            call("chat.setAdmin", {**dialog, "user": user_id, "isAdmin": action == "make_admin"},
                 "only group admins can change admins")
    elif action == "make_private":
        call("chat.convertDialogToNotPublic", dialog, "only group admins can change this")
    elif action == "remove_photo":
        call("chat.removePhoto", dialog, "only group admins can change the photo")
    else:
        full = chat_full(conversation_id)
        if full.get("is_project_group"):
            raise ToolError("This is a project conversation: archive the project with mizito_archive_project instead")
        if not full.get("is_group"):
            raise ToolError("Only groups can be deleted")
        require_confirm(confirm, full.get("title"), "group")
        call("chat.deleteDialog", dialog, "only group admins can delete a group")
    return {"conversation_id": conversation_id, "action": action, "done": True}


@tool("ساخت گروه گفتگو", kind="create")
def mizito_create_group(
    title: Annotated[str, Field(description="Group name.")],
    member_ids: UserIds,
    is_public: Annotated[bool, Field(description="Public groups (گروه عمومی) include every workspace member automatically.")] = False,
) -> dict:
    """Create a group conversation (گروه گفتگو) with the given members; you become its admin. For a project
    with tasks use mizito_create_project instead (it creates the project conversation too)."""
    payload = {"title": title, "is_public": is_public, "is_project_group": False, "members": member_ids}
    dialog = client.call("chat.createDialog", payload) or {}
    if not isinstance(dialog, dict) or not dialog.get("_id"):
        raise ToolError("Mizito did not create the group (no permission to create groups?)")
    return {"conversation_id": dialog["_id"], "title": dialog.get("title") or title}


@tool("اعضا و تنظیمات یک گفتگو")
def mizito_get_conversation(conversation_id: ConversationId) -> dict:
    """Details of one conversation: title, type (private, group, public group, project, customer file),
    members with admins, whether notifications are muted, the linked project and open tasks posted in it."""
    full = chat_full(conversation_id)
    row = dialog_row(conversation_id)
    participants = full.get("participants") or []
    ids = [p.get("user_id") if isinstance(p, dict) else p for p in participants]
    admins = set(full.get("group_admins") or row.get("group_admins") or [])
    try:
        undone = client.call("chat.getDialogUnDoneTasksCount", {"dialog": conversation_id})
    except MizitoError:
        undone = None
    return compact({
        "conversation_id": conversation_id,
        "title": client.dialog_title(row),
        "is_group": full.get("is_group"),
        "is_public_group": full.get("is_public_group"),
        "is_channel": row.get("is_channel"),
        "is_project_conversation": full.get("is_project_group"),
        "is_customer_file": full.get("is_customer_entity"),
        "project_id": row.get("project_entity"),
        "muted": (full.get("settings") or {}).get("mute"),
        "members": [compact({"id": u, "name": client.user_name(u), "admin": u in admins or None}) for u in ids if u],
        "open_tasks_in_conversation": undone,
    })

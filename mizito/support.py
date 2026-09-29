"""Chat with Mizito's own support team (پشتیبانی میزیتو) and product suggestions."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mizito.app import ToolError, call, check, client, compact, html_text, html_to_text, jalali, tool


@tool("گفتگوی پشتیبانی میزیتو")
def mizito_support_history() -> dict:
    """Your conversation with Mizito's support team (the company behind Mizito, not your colleagues): past
    questions and answers and how many answers are unread."""
    rows = call("support.clientOnlineHistory", {}) or []
    messages = [compact({
        "id": r.get("_id"),
        "from": "support" if r.get("is_response") else "me",
        "date_jalali": jalali(r.get("send_date") or r.get("date")),
        "text": html_to_text(r.get("message")),
    }) for r in rows if isinstance(r, dict)]
    unread = client.call("support.getClientUnreadCount", {})
    return {"unread": unread, "count": len(messages), "messages": messages}


@tool("پیام به پشتیبانی میزیتو", kind="create")
def mizito_contact_support(
    action: Annotated[Literal["send", "edit", "delete", "suggestion"], Field(description=(
        "send = message to Mizito support; edit / delete = your own earlier support message (message_id); "
        "suggestion = a product suggestion or consultation request (subject + text)."))],
    text: Annotated[str | None, Field(description="Message or suggestion text.")] = None,
    message_id: Annotated[str | None, Field(description="For edit/delete: id from mizito_support_history.")] = None,
    subject: Annotated[str, Field(description="For suggestion: subject.")] = "درخواست مشاوره",
) -> dict:
    """Write to Mizito's support team (outside your workspace) or send them a suggestion. Only on the user's
    explicit request."""
    if action in ("send", "edit", "suggestion") and not text:
        raise ToolError("text is required")
    if action in ("edit", "delete") and not message_id:
        raise ToolError("message_id is required")
    if action == "send":
        result = call("support.sendFromClient", {"message": html_text(text), "media": None, "replyTo": None})
    elif action == "edit":
        result = call("support.editFromClient", {"messageId": message_id, "message": html_text(text)})
    elif action == "delete":
        result = call("support.deleteFromClient", {"messageId": message_id})
    else:
        result = check(call("support.sendSuggestion", {"subject": subject, "content": text}), "send the suggestion")
    return {"action": action, "done": True, "result": compact(result)}

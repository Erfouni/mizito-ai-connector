"""Personal notes (یادداشت) and labels (برچسب)."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mizito.app import Confirm, LabelIds, ToolError, call, check, client, compact, jalali, require_confirm, tool

NoteColor = Annotated[Literal["white", "red", "orange", "yellow", "grey", "blue", "cyan", "green"], Field(description="Note color.")]
LabelKind = Annotated[Literal["task", "inbox", "note", "project", "customer", "deal", "payment", "minute"], Field(
    description="What the labels are for: task, inbox (letters), note, project (project groups), customer, deal, payment, minute.")]
NoteId = Annotated[str, Field(description="Note id (`_id`) from mizito_list_notes.")]
# Mizito's internal label types; the tools use friendlier names for two of them.
LABEL_TYPES = {"task": "task", "inbox": "inbox", "note": "notes", "project": "project", "customer": "crm",
               "deal": "deal", "payment": "payment", "minute": "minute"}


@tool("یادداشت‌های من")
def mizito_list_notes(
    archived: Annotated[bool, Field(description="List archived notes instead of active ones.")] = False,
) -> dict:
    """Your personal notes (یادداشت‌ها): title, text, color, checklist, labels and pin state. Nobody else sees
    them."""
    notes = client.call("notes.getAll", {"archived": True} if archived else {}) or []
    for note in notes:
        if isinstance(note, dict):
            for key in ("created_at", "modified_at", "updated_at"):
                if note.get(key):
                    note[f"{key}_jalali"] = jalali(note[key])
    return {"archived": archived, "count": len(notes), "notes": compact(notes)}


def _find_note(note_id: str) -> dict:
    for query in ({}, {"archived": True}):
        for note in client.call("notes.getAll", query) or []:
            if note.get("_id") == note_id:
                return note
    raise ToolError(f"Note {note_id!r} not found")


@tool("ساخت یادداشت", kind="create")
def mizito_create_note(
    title: Annotated[str, Field(description="Note title.")],
    text: Annotated[str, Field(description="Note body.")] = "",
    color: NoteColor = "white",
    checklist: Annotated[list[str] | None, Field(description="Checklist item titles.")] = None,
    label_ids: LabelIds = None,
) -> dict:
    """Create a personal note (یادداشت), optionally with a checklist and labels (kind='note')."""
    payload = {"title": title, "note": text, "photo": None, "color": color, "labels": label_ids or [],
               "checklist": [{"checked": False, "title": item} for item in checklist or []]}
    return {"created": True, "note": compact(client.call("notes.create", payload))}


@tool("ویرایش یادداشت", kind="update")
def mizito_update_note(
    note_id: NoteId,
    title: Annotated[str | None, Field(description="New title.")] = None,
    text: Annotated[str | None, Field(description="New body (replaces the old one).")] = None,
    color: Annotated[Literal["white", "red", "orange", "yellow", "grey", "blue", "cyan", "green"] | None, Field(description="New color.")] = None,
    label_ids: Annotated[list[str] | None, Field(description="New label list (replaces the current one).")] = None,
    add_checklist_items: Annotated[list[str] | None, Field(description="Checklist items to append.")] = None,
) -> dict:
    """Edit a note's title, text, color, labels or checklist. Omitted fields stay as they are."""
    note = _find_note(note_id)
    payload = {k: note.get(k) for k in ("_id", "title", "note", "photo", "color", "checklist", "labels") if k in note}
    payload.update({k: v for k, v in (("title", title), ("note", text), ("color", color)) if v is not None})
    if add_checklist_items:
        payload["checklist"] = list(note.get("checklist") or []) + [{"checked": False, "title": t} for t in add_checklist_items]
    result = client.call("notes.update", payload)
    if label_ids is not None:
        client.call("notes.setLabels", {"note_id": note_id, "labels": label_ids})
        result = _find_note(note_id)
    return {"note": compact(result)}


@tool("مدیریت یادداشت (آرشیو، سنجاق، حذف، چک‌لیست)", kind="update")
def mizito_manage_note(
    note_id: NoteId,
    action: Annotated[Literal["archive", "unarchive", "pin", "unpin", "delete", "restore", "check_item", "uncheck_item"], Field(description=(
        "archive / unarchive; pin / unpin to the top; delete moves it to the trash (restore brings it back); "
        "check_item / uncheck_item tick a checklist item (item_index)."))],
    item_index: Annotated[int | None, Field(description="0-based checklist item index, for check_item / uncheck_item.", ge=0)] = None,
) -> dict:
    """Archive, pin, delete/restore a note or tick its checklist items."""
    if action in ("archive", "unarchive"):
        client.call("notes.archiveNote", {"note_id": note_id, "archived": action == "archive"})
    elif action in ("pin", "unpin"):
        client.call("notes.updatePinState", {"pinned": action == "pin", "noteId": note_id})
    elif action in ("delete", "restore"):
        client.call("notes.deleteNote", {"note_id": note_id, "deleted": action == "delete"})
    else:
        if item_index is None:
            raise ToolError("item_index is required for check_item/uncheck_item")
        client.call("notes.setChecklistValue", {"note_id": note_id, "check_index": item_index,
                                                "checked": action == "check_item"})
    return {"note_id": note_id, "action": action, "done": True}


# --- labels --------------------------------------------------------------------------------------


@tool("برچسب‌ها")
def mizito_list_labels(kind: LabelKind = "task") -> dict:
    """Labels (برچسب‌ها) of one kind with their ids and colors, for tagging tasks, letters, notes, projects,
    customers, deals, payments or minutes."""
    data = client.call("labels.getAll", {"type": LABEL_TYPES[kind]}) or {}
    return {"kind": kind, "labels": compact(data.get("labels") or [])}


@tool("ساخت برچسب", kind="create")
def mizito_create_label(
    title: Annotated[str, Field(description="Label name.")],
    kind: LabelKind = "task",
    color: Annotated[str, Field(description="Label color name, e.g. grey, red, orange, yellow, green, cyan, blue, purple.")] = "grey",
) -> dict:
    """Create a label (برچسب). Some label kinds can only be created by workspace admins."""
    result = call("labels.add", {"title": title, "color": color, "type": LABEL_TYPES[kind]},
                  "only workspace admins can add some label kinds")
    check(result, "create the label (only workspace admins can add some label kinds)")
    labels = (client.call("labels.getAll", {"type": LABEL_TYPES[kind]}) or {}).get("labels") or []
    created = next((l for l in labels if l.get("title") == title), None)
    return {"created": True, "label": compact(created or result)}


@tool("ویرایش یا حذف برچسب", kind="update")
def mizito_manage_label(
    label_id: Annotated[str, Field(description="Label id from mizito_list_labels.")],
    kind: LabelKind,
    action: Annotated[Literal["rename", "recolor", "delete", "history"], Field(description=(
        "rename (title) / recolor (color); delete removes the label from every item (irreversible, confirm = its "
        "title); history = who changed it."))],
    title: Annotated[str | None, Field(description="New name, for rename.")] = None,
    color: Annotated[str | None, Field(description="New color, for recolor.")] = None,
    confirm: Confirm = None,
) -> dict:
    """Rename, recolor or delete a label, or see its change history. Workspace-wide labels need admin rights."""
    labels = (client.call("labels.getAll", {"type": LABEL_TYPES[kind]}) or {}).get("labels") or []
    label = next((l for l in labels if l.get("_id") == label_id), None)
    if not label:
        raise ToolError(f"Label {label_id!r} not found among {kind} labels")
    if action == "history":
        return {"label": compact(label), "history": compact(call("labels.history", {"label_id": label_id}) or [])}
    if action == "delete":
        require_confirm(confirm, label.get("title"), "label")
        check(call("labels.delete", {"label_id": label_id, "label_type": LABEL_TYPES[kind]}), "delete the label")
        return {"deleted": True, "label_id": label_id}
    new_title = title if action == "rename" else label.get("title")
    new_color = color if action == "recolor" else label.get("color")
    if not new_title or not new_color:
        raise ToolError("title is required for rename, color for recolor")
    check(call("labels.save", {"label_id": label_id, "type": LABEL_TYPES[kind], "title": new_title, "color": new_color},
               "only workspace admins can edit shared labels"), "save the label")
    return {"label": compact({**label, "title": new_title, "color": new_color})}

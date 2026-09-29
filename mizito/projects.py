"""Projects: listing, overview, creation, members, kanban boards, advanced features, files, archive, clone."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mizito.app import (
    ADVANCED_FIELDS, ProjectId, ToolError, UserIds, call, check, client, compact, file_ref, jalali, project_full,
    project_overview, projects_tab, tool,
)
from mizito_client import MizitoError

PLAN_HINT = "the workspace plan may not include this, or project admin rights are needed"


@tool("فهرست پروژه‌ها")
def mizito_list_projects() -> dict:
    """Projects of the active workspace with their ids, colors and members. has_conversation/in_projects_tab
    are false for projects made without a project conversation (web-app «دسته‌بندی»): they exist and hold tasks,
    but the web app's Projects tab does not show them."""
    data = client.call("projects.getList", {}) or {}
    tab = projects_tab()
    projects = []
    for p in data.get("projects") or []:
        row = compact(p)
        row["has_conversation"] = bool(p.get("dialog"))
        row["in_projects_tab"] = p.get("_id") in tab
        projects.append(row)
    return {"count": len(projects), "projects": projects, "statuses": compact(data.get("project_status") or [])}


@tool("نمای کامل یک پروژه")
def mizito_get_project(project_id: ProjectId) -> dict:
    """Everything about one project: owner, members and admins (with names), kanban boards with per-board task
    counts, labels, its project conversation, whether the Projects tab shows it, archive state, advanced
    features and task statistics (mine/others, overdue, today, done). Use it to verify changes."""
    out = project_overview(project_id)
    if out.get("conversation_id"):
        try:
            summary = client.call("projects.chatSummary", {"dialog": out["conversation_id"], "project": project_id,
                                                           "withBoards": True}) or {}
            titles = {b["id"]: b.get("title") for b in out.get("boards") or []}
            out["board_stats"] = [  # "null" = tasks on the project's default board
                compact({"board": titles.get(bid) or ("برای انجام (پیش‌فرض)" if bid in ("null", None) else bid),
                         "board_id": None if bid == "null" else bid, **stats})
                for bid, stats in (summary.get("boards") or {}).items()]
        except MizitoError:
            pass
    return out


# --- write tools ---------------------------------------------------------------------------------


@tool("ساخت پروژه", kind="create")
def mizito_create_project(
    title: Annotated[str, Field(description="Project name.")],
    member_ids: Annotated[list[str] | None, Field(description="Members besides you (ids from mizito_list_users).")] = None,
    color: Annotated[str, Field(description="Project color, e.g. grey, red, orange, yellow, green, cyan, blue, purple.")] = "grey",
) -> dict:
    """Create a project exactly like the web app's «ایجاد پروژه» button: the project plus its project
    conversation, with you as owner/admin and member_ids as members. It shows in the Projects tab. Returns
    project_id and conversation_id. Only on the user's explicit request."""
    me = client.my_user_id()
    payload = {"title": title, "is_public": False, "is_project_group": True,
               "members": [m for m in member_ids or [] if m != me], "color": color}
    dialog = client.call("chat.createDialog", payload) or {}
    project_id = dialog.get("project_entity") if isinstance(dialog, dict) else None
    if not project_id and isinstance(dialog, dict) and dialog.get("_id"):
        project_id = next((p["_id"] for p in (client.call("projects.getList", {}) or {}).get("projects", [])
                           if p.get("dialog") == dialog["_id"]), None)
    if not project_id:
        raise ToolError("Mizito did not create the project (no permission to create projects?)")
    return {"created": True, "project_id": project_id, "conversation_id": dialog.get("_id"),
            "project": project_overview(project_id)}


@tool("ویرایش پروژه", kind="update")
def mizito_update_project(
    project_id: ProjectId,
    title: Annotated[str | None, Field(description="New name.")] = None,
    color: Annotated[str | None, Field(description="New color name.")] = None,
    member_ids: Annotated[list[str] | None, Field(description="The complete new member list (include everyone who should stay). To only add people use mizito_add_project_members.")] = None,
    label_ids: Annotated[list[str] | None, Field(description="Project labels/groups (گروه‌بندی پروژه), ids from mizito_list_labels(kind='project'); replaces the current ones.")] = None,
) -> dict:
    """Rename a project, change its color, replace its members or set its labels. Omitted fields stay as
    they are. Needs project admin rights. Members removed from a project lose access to its conversation."""
    full = project_full(project_id)
    dialog = full.get("dialog")
    if dialog:  # the web app edits project conversations through the conversation
        if title is not None and title != full.get("title"):
            call("chat.updateTitle", {"dialog": dialog, "title": title}, "only project admins can rename")
        if color is not None and color != full.get("color"):
            call("projects.setChatProjectColor", {"project": project_id, "dialog": dialog, "color": color}, PLAN_HINT)
        if member_ids is not None:
            current = set(full.get("members") or [])
            wanted = set(member_ids) | {client.my_user_id()}
            for user in sorted(wanted - current):
                call("chat.inviteUser", {"dialog": dialog, "user": user}, "only project admins can add members")
            for user in sorted(current - wanted):
                call("chat.deleteUser", {"dialog": dialog, "user": user}, "only project admins can remove members")
        if label_ids is not None:
            call("projects.setChatProjectLabels", {"project": project_id, "dialog": dialog, "labels": label_ids}, PLAN_HINT)
    else:
        if label_ids is not None:
            raise ToolError("Labels can only be set on projects that have a project conversation")
        payload = {
            "project_id": project_id,
            "title": title if title is not None else full.get("title"),
            "color": color or full.get("color") or "grey",
            "members": member_ids if member_ids is not None else list(full.get("members") or []),
        }
        check(client.call("projects.save", payload), "change the project (only project admins can edit it)")
    return {"project": project_overview(project_id)}


@tool("افزودن عضو به پروژه", kind="create")
def mizito_add_project_members(project_id: ProjectId, user_ids: UserIds) -> dict:
    """Add workspace members to a project (they are notified by Mizito). For people without a Mizito
    account use mizito_invite_workspace_member first."""
    full = project_full(project_id)
    current = list(full.get("members") or [])
    new = [u for u in user_ids if u not in current]
    if full.get("dialog"):
        for user in new:  # project members are the members of the project conversation
            call("chat.inviteUser", {"dialog": full["dialog"], "user": user}, "only project admins can add members")
    elif new:
        payload = {"project_id": project_id, "title": full.get("title"), "color": full.get("color") or "grey",
                   "members": current + new}
        check(client.call("projects.save", payload), "add members (only project admins can)")
    return {"added": len(new), "project": project_overview(project_id)}


@tool("افزودن ستون (لیست) کانبان", kind="create")
def mizito_add_project_board(
    project_id: ProjectId,
    title: Annotated[str, Field(description="Board (column) name, e.g. «در حال انجام».")],
    color: Annotated[str, Field(description="Board color name.")] = "grey",
) -> dict:
    """Add a kanban board / column (ستون، لیست) to a project. Tasks are grouped by these boards; move tasks
    between them with mizito_move_task_to_board."""
    result = client.call("projects.addKanbanBoard", {"projectId": project_id, "kanbanBoard": [{"title": title, "color": color}]})
    check(result, "add the board (project admin rights needed?)")
    return {"project": compact({k: v for k, v in project_overview(project_id).items() if k in ("project_id", "title", "boards")})}


@tool("مدیریت ستون‌های کانبان", kind="update")
def mizito_manage_project_board(
    project_id: ProjectId,
    board_id: Annotated[str, Field(description="Board id from mizito_get_project's boards.")],
    action: Annotated[Literal["rename", "recolor", "move", "sort_tasks", "delete"], Field(description=(
        "rename (title) / recolor (color); move = change the board's position (position, 0 = first); sort_tasks = "
        "reorder the board's tasks once by sort_by/order; delete = remove an empty board (not the default one)."))],
    title: Annotated[str | None, Field(description="New board name, for rename.")] = None,
    color: Annotated[str | None, Field(description="New color, for recolor.")] = None,
    position: Annotated[int | None, Field(description="New 0-based position among the boards, for move.", ge=0)] = None,
    sort_by: Annotated[Literal["reminder", "created", "modified"], Field(description="For sort_tasks: reminder time, creation or last change.")] = "reminder",
    order: Annotated[Literal["asc", "desc"], Field(description="For sort_tasks: ascending or descending.")] = "asc",
) -> dict:
    """Rename, recolor, reorder, sort or delete a project's kanban board. Needs project admin rights."""
    full = project_full(project_id)
    boards = full.get("kanban_boards") or []
    index = next((i for i, b in enumerate(boards) if b.get("_id") == board_id), None)
    if index is None:
        raise ToolError(f"Board {board_id!r} is not in this project (see mizito_get_project)")
    board = {k: v for k, v in boards[index].items() if k != "tasks"}
    if action in ("rename", "recolor"):
        if action == "rename" and not title:
            raise ToolError("title is required for rename")
        if action == "recolor" and not color:
            raise ToolError("color is required for recolor")
        board.update({"title": title} if action == "rename" else {"color": color})
        call("projects.updateKanbanBoard", {"projectId": project_id, "kanbanBoardId": board_id, "kanbanBoard": board}, PLAN_HINT)
    elif action == "move":
        if position is None:
            raise ToolError("position is required for move")
        new = min(position, len(boards) - 1)
        call("projects.setKanbanBoardOrder", {"projectId": project_id, "boardId": board_id,
                                              "oldPosition": index, "newPosition": new}, PLAN_HINT)
    elif action == "sort_tasks":
        field = {"reminder": "alarm_at", "created": "created_at", "modified": "modified_at"}[sort_by]
        call("tasks.setKanbanWeightSort", {"projectId": project_id, "kanbanBoardId": board_id,
                                           "sortField": field, "sortOrder": order}, PLAN_HINT)
    else:
        if board.get("is_default") or index == 0 and not full.get("kanban_boards_processed"):
            raise ToolError("The default board cannot be deleted")
        check(call("projects.removeKanbanBoard", {"projectId": project_id, "boardId": board_id},
                   "a board that still has open tasks cannot be deleted"), "delete the board")
    return {"action": action, "done": True,
            "boards": project_overview(project_id).get("boards")}


@tool("آرشیو پروژه", kind="update")
def mizito_archive_project(
    project_id: ProjectId,
    with_tasks: Annotated[bool, Field(description="Also archive the project's tasks.")] = False,
) -> dict:
    """Archive a project, like the web app's archive dialog. Members lose it from their lists; a workspace
    admin can restore it (mizito_admin_restore_project). Projects without a project conversation can only
    be archived by a workspace admin."""
    full = project_full(project_id)
    if not full.get("dialog"):
        raise ToolError("This project has no project conversation; only a workspace admin can archive it "
                        "(mizito_admin_archive_category)")
    client.call("chat.archiveProject", {"dialog": full["dialog"], "project": project_id, "withArchiveTasks": with_tasks})
    # An archived project drops out of projects.getList (and projects.full answers 400 for it).
    still_listed = any(p.get("_id") == project_id for p in (client.call("projects.getList", {}) or {}).get("projects", []))
    if still_listed:
        raise ToolError("Mizito did not archive the project (project admin rights needed?)")
    return {"archived": True, "project_id": project_id, "title": full.get("title"), "tasks_archived": with_tasks}


@tool("کپی گرفتن از پروژه", kind="create")
def mizito_clone_project(
    project_id: ProjectId,
    new_title: Annotated[str, Field(description="Name of the copy.")],
    skip_task_ids: Annotated[list[str] | None, Field(description="Task ids (from mizito_list_tasks(scope='project')) NOT to copy; by default every open task is copied.")] = None,
) -> dict:
    """Duplicate a project (کپی پروژه) with its boards, members and tasks into a new project with its own
    conversation. Only on the user's explicit request."""
    project_full(project_id)
    result = call("projects.clone", {"projectId": project_id, "projectName": new_title, "ignoreTaskIds": skip_task_ids or []},
                  PLAN_HINT)
    dialog = result if isinstance(result, str) else (result or {}).get("_id") if isinstance(result, dict) else None
    new_id = next((p["_id"] for p in (client.call("projects.getList", {}) or {}).get("projects", [])
                   if dialog and p.get("dialog") == dialog), None)
    if not new_id:
        new_id = next((p["_id"] for p in (client.call("projects.getList", {}) or {}).get("projects", [])
                       if p.get("title") == new_title), None)
    if not new_id:
        raise ToolError(f"Mizito did not report the copy: {result!r}")
    return {"created": True, "project_id": new_id, "project": project_overview(new_id)}


FEATURE_NAMES = {
    "gantt": "advanced_support_gantt",
    "automation": "advanced_support_automation",
    "advanced_minutes": "advanced_minutes",
    "task_weights": "advanced_tasks_has_weight",
    "weighted_progress": "advanced_project_summary_with_weight",
    "only_admins_edit_tasks": "advanced_tasks_edit_only_admins",
    "members_cannot_snooze": "advanced_tasks_prevent_snooze_by_users",
    "admin_confirms_done_tasks": "advanced_duplicate_confirm",
    "deadline_required": "advanced_has_deadline",
    "members_can_create_tasks": "advanced_public_create_task",
}


@tool("فعال‌سازی امکانات پیشرفته‌ی پروژه (گانت، اتوماسیون...)", kind="update")
def mizito_set_project_advanced(
    project_id: ProjectId,
    enabled: Annotated[bool | None, Field(description="Turn the project's advanced features (پروژه‌ی پیشرفته) on or off.")] = None,
    features: Annotated[dict[str, bool] | None, Field(description=(
        "Switch individual advanced features on/off: gantt, automation, advanced_minutes, task_weights, "
        "weighted_progress, only_admins_edit_tasks, members_cannot_snooze, admin_confirms_done_tasks "
        "(tasks go to the board admin before being done), deadline_required, members_can_create_tasks. "
        'Example: {"gantt": true, "automation": true}.'))] = None,
    admin_ids: Annotated[list[str] | None, Field(description="Advanced-project admins (replaces the list).")] = None,
    gantt_viewer_ids: Annotated[list[str] | None, Field(description="Who may view the Gantt chart (replaces the list).")] = None,
    monitoring_viewer_ids: Annotated[list[str] | None, Field(description="Who may view project monitoring reports (replaces the list).")] = None,
) -> dict:
    """Enable advanced project features and choose which ones are active: Gantt chart, automation, advanced
    minutes, task weights, approval of done tasks and more. Needs a project conversation, project admin
    rights and a plan with advanced projects. Returns the resulting feature state."""
    full = project_full(project_id)
    dialog = full.get("dialog")
    if not dialog:
        raise ToolError("Advanced features need a project with a project conversation")
    unknown = set(features or {}) - set(FEATURE_NAMES)
    if unknown:
        raise ToolError(f"Unknown features {sorted(unknown)}; use {sorted(FEATURE_NAMES)}")
    if enabled is not None and bool(full.get("is_advanced")) != enabled:
        call("projects.activateAdvancedFeatures", {"project": project_id, "dialog": dialog, "advanced": enabled},
             "advanced projects need an enterprise/advanced plan and project admin rights")
    if features or admin_ids is not None or gantt_viewer_ids is not None or monitoring_viewer_ids is not None:
        full = project_full(project_id)
        params = {"project": project_id, "is_advanced": full.get("is_advanced"),
                  "automation_mode": full.get("automation_mode") or "classic",
                  "members_admin": admin_ids if admin_ids is not None else list(full.get("members_admin") or []),
                  "gantt_viewers": gantt_viewer_ids if gantt_viewer_ids is not None else list(full.get("gantt_viewers") or []),
                  "monitoring_viewers": monitoring_viewer_ids if monitoring_viewer_ids is not None else list(full.get("monitoring_viewers") or [])}
        params.update({k: full.get(k) for k in ADVANCED_FIELDS})
        params.update({FEATURE_NAMES[k]: v for k, v in (features or {}).items()})
        call("projects.setAdvancedFeatures", {"dialog": dialog, "advanced": params},
             "advanced projects need an enterprise/advanced plan and project admin rights")
    after = project_full(project_id)
    return compact({"project_id": project_id, "is_advanced": bool(after.get("is_advanced")),
                    "features": {name: bool(after.get(field)) for name, field in FEATURE_NAMES.items()},
                    "admins": [client.user_name(u) for u in after.get("members_admin") or []]})


@tool("فایل‌های پروژه")
def mizito_list_project_files(
    project_id: ProjectId,
    file_name: Annotated[str | None, Field(description="Only files whose name contains this text.")] = None,
    offset: Annotated[int, Field(description="Skip this many files (paging).", ge=0)] = 0,
) -> dict:
    """Files attached anywhere in a project (its conversation and its tasks), newest first, with file_id for
    mizito_read_file / mizito_get_file_link and where each file was attached."""
    payload = {"project": project_id, "filterType": "filename" if file_name else None, "fromIndex": offset}
    if file_name:
        payload["filename"] = file_name
    rows = call("projects.getProjectFiles", payload, PLAN_HINT) or []
    files = []
    for row in rows:
        attachment = row.get("attachment") or {}
        media = attachment.get("media") if isinstance(attachment.get("media"), dict) else attachment
        obj = next((media[k] for k in ("document", "photo", "video", "audio") if isinstance(media.get(k), dict)), media)
        files.append(compact({**file_ref(obj), "date_jalali": jalali(row.get("attach_at") or attachment.get("attach_at")),
                              "task_id": row.get("task"), "message_id": row.get("message"),
                              "by": client.user_name(row.get("user") or attachment.get("user"))}))
    return {"project_id": project_id, "offset": offset, "count": len(files), "files": files}

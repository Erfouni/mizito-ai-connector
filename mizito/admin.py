"""Workspace administration (مدیریت میزکار): members, roles, permissions, settings, access repair and
hand-over of a departing member's work. Registered only with MIZITO_ENABLE_ADMIN=1; the logged-in user
must be a workspace admin."""
from __future__ import annotations

import time
from typing import Annotated, Literal

from pydantic import Field

from mizito.app import Confirm, ProjectId, ToolError, UserId, UserIds, call, check, client, compact, names, require_confirm, tool

HINT = "only workspace admins (or the owner) can do this"
ROLES = {"member": 0, "admin": 1, "guest": 2}


@tool("مدیریت اعضای میزکار (نقش، دسترسی، حذف)", kind="update", feature="admin")
def mizito_admin_manage_member(
    user_id: UserId,
    action: Annotated[Literal["set_role", "set_position", "grant_permission", "revoke_permission", "remove", "rejoin"], Field(description=(
        "set_role (role); set_position = job title shown next to the name (position; needs positions enabled); "
        "grant_permission / revoke_permission (permission); remove = take the member out of the workspace "
        "(confirm = their name; rejoin can undo it); rejoin = bring a removed member back."))],
    role: Annotated[Literal["member", "admin", "guest"] | None, Field(description="For set_role. Guests need an advanced plan.")] = None,
    position: Annotated[str | None, Field(description="For set_position: e.g. «مدیر فروش».")] = None,
    permission: Annotated[Literal["project_creator", "chat_group_creator", "crm_creator"] | None, Field(description=(
        "For grant/revoke: may create projects, groups or CRM files (effective when the matching "
        "only_selected_can_* setting is on in mizito_admin_workspace_settings)."))] = None,
    confirm: Confirm = None,
) -> dict:
    """Change a workspace member's role, job title or creation rights, remove them from the workspace or
    bring them back. Only on the user's explicit request."""
    if action == "set_role":
        if not role:
            raise ToolError("role is required for set_role")
        result = call("workspace.changeRole", {"user_id": user_id, "role": ROLES[role]}, HINT)
        if isinstance(result, dict) and result.get("msg"):
            raise ToolError(f"Mizito refused: {result['msg']}")
    elif action == "set_position":
        call("workspace.updateWorkspaceRoleName", {"user_id": user_id, "workspaceRoleName": position or ""}, HINT)
    elif action in ("grant_permission", "revoke_permission"):
        if not permission:
            raise ToolError("permission is required")
        call("workspace.updateUserPermission", {"user": user_id, "permission": permission,
                                                "access": action == "grant_permission"}, HINT)
    elif action == "remove":
        require_confirm(confirm, client.user_name(user_id), "member")
        call("workspace.removeMember", {"member_id": user_id}, HINT)
    else:
        check(call("workspace.reJoinMember", {"member_id": user_id}, HINT), "bring the member back")
    return {"user": client.user_name(user_id), "action": action, "done": True}


@tool("تنظیمات میزکار", kind="update", feature="admin")
def mizito_admin_workspace_settings(
    title: Annotated[str | None, Field(description="New workspace name.")] = None,
    only_selected_can_create_projects: Annotated[bool | None, Field(description="Only members with the project_creator permission may create projects.")] = None,
    only_selected_can_create_groups: Annotated[bool | None, Field(description="Only members with chat_group_creator may create groups.")] = None,
    only_selected_can_create_crm: Annotated[bool | None, Field(description="Only members with crm_creator may create customer files.")] = None,
    positions_enabled: Annotated[bool | None, Field(description="Show job titles (سمت‌های سازمانی) next to member names.")] = None,
) -> dict:
    """Rename the workspace or change who may create projects, groups and customer files, and whether job
    titles are shown. Returns the current permissions."""
    if title:
        call("workspace.updateTitle", {"title": title}, HINT)
    for key, value in (("en_custom_project_creators", only_selected_can_create_projects),
                       ("en_custom_chat_group_creators", only_selected_can_create_groups),
                       ("en_custom_crm_creators", only_selected_can_create_crm),
                       ("en_support_workspace_roles", positions_enabled)):
        if value is not None:
            call("workspace.setWorkspaceSettings", {"title": key, "value": value}, HINT)
    perms = call("workspace.getPermissions", {}, HINT) or {}
    return {"name": client.call("workspace.name", {}), "permissions": compact(perms)}


_FIX = {"projects": ("fix.projects", "projectIds", "project"), "groups": ("fix.chatGroups", "dialogIds", "dialog"),
        "customers": ("fix.customer", "customerIds", "customer")}


@tool("همه‌ی پروژه‌ها، گروه‌ها و پرونده‌ها (نمای مدیر)", feature="admin")
def mizito_admin_list_all(
    kind: Annotated[Literal["projects", "groups", "customers"], Field(description="What to list across the whole workspace.")],
    has_member_id: Annotated[str | None, Field(description="Only items this member can access.")] = None,
    without_member_id: Annotated[str | None, Field(description="Only items this member can NOT access.")] = None,
    archive: Annotated[Literal["all", "archived", "active"], Field(description="Archived state filter.")] = "all",
    members_of: Annotated[str | None, Field(description="Instead of listing: return the members of this project/group/customer id.")] = None,
) -> dict:
    """Admin view (ابزار اصلاح دسترسی) of every project, group or customer file in the workspace, including
    ones you are not a member of, with their members and archive state. Use it with mizito_admin_grant_access
    to repair access."""
    prefix, _, single = _FIX[kind]
    if members_of:
        members = call(f"{prefix}.getMembers", {single: members_of}, HINT) or []
        return {"kind": kind, "id": members_of, "members": compact(members),
                "member_names": names([m if isinstance(m, str) else m.get("_id") or m.get("user") for m in members])}
    flt = {"access": has_member_id, "access_not": without_member_id,
           "archive_status": {"all": 0, "archived": 1, "active": 2}[archive]}
    if kind == "projects":
        flt["project_labels"] = []
    rows = call(f"{prefix}.getAll", {"filter": flt}, HINT) or []
    return {"kind": kind, "count": len(rows), "items": compact(rows)}


@tool("دادن یا گرفتن دسترسی (نمای مدیر)", kind="update", feature="admin")
def mizito_admin_grant_access(
    kind: Annotated[Literal["projects", "groups", "customers"], Field(description="Kind of the items.")],
    item_ids: Annotated[list[str], Field(description="Project, group (conversation) or customer ids from mizito_admin_list_all.")],
    user_ids: UserIds,
    access: Annotated[bool, Field(description="true = give these members access, false = take it away.")],
) -> dict:
    """Give or remove members' access to projects, groups or customer files in bulk, as a workspace admin,
    without being a member yourself. Only on the user's explicit request."""
    prefix, key, _ = _FIX[kind]
    call(f"{prefix}.grantAccess", {key: item_ids, "users": user_ids, "access": access}, HINT)
    return {"kind": kind, "items": len(item_ids), "users": names(user_ids), "access": access, "done": True}


@tool("انتقال کارهای یک عضو به عضو دیگر", kind="update", feature="admin")
def mizito_admin_transfer_member_work(
    from_user_id: Annotated[str, Field(description="Member whose work is handed over (e.g. someone leaving).")],
    to_user_id: Annotated[str, Field(description="Member who takes it over.")],
    tasks: Annotated[bool, Field(description="Move their tasks.")] = True,
    groups: Annotated[bool, Field(description="Move their group memberships.")] = True,
    customers: Annotated[bool, Field(description="Move their customer files.")] = True,
    history_only: Annotated[bool, Field(description="Only show previous transfers, change nothing.")] = False,
) -> dict:
    """Hand over a member's tasks, group memberships and customer files to another member (جابجایی کاربر),
    e.g. when someone leaves. Cannot be undone automatically. Only on the user's explicit request."""
    if history_only:
        return {"history": compact(call("fix.changeUser.history", {}, HINT) or [])}
    if from_user_id == to_user_id:
        raise ToolError("from_user_id and to_user_id must differ")
    if not (tasks or groups or customers):
        raise ToolError("Choose at least one of tasks, groups, customers")
    done = []
    for flag, endpoint, label in ((tasks, "fix.changeUser.changeTasks", "tasks"),
                                  (groups, "fix.changeUser.changeChatGroups", "groups"),
                                  (customers, "fix.changeUser.changeCustomers", "customers")):
        if flag:
            call(endpoint, {"fromUser": from_user_id, "toUser": to_user_id}, HINT)
            done.append(label)
            time.sleep(1)  # the web app spaces these calls out
    return {"from": client.user_name(from_user_id), "to": client.user_name(to_user_id), "moved": done}


@tool("بازگردانی پروژه‌ی آرشیوشده", kind="update", feature="admin")
def mizito_admin_restore_project(
    project_id: Annotated[str, Field(description="Archived project id from mizito_admin_list_all(kind='projects', archive='archived').")],
    member_ids: UserIds,
    restore_tasks: Annotated[bool, Field(description="Also restore the tasks archived with it.")] = True,
) -> dict:
    """Restore an archived project (with a project conversation) by giving its members access again, and
    optionally restore its archived tasks."""
    call("fix.projects.grantAccess", {"projectIds": [project_id], "users": member_ids, "access": True}, HINT)
    if restore_tasks:
        call("projects.restoreArchivedTasks", {"project": project_id}, HINT)
    return {"project_id": project_id, "members": names(member_ids), "tasks_restored": restore_tasks}


@tool("آرشیو دسته‌بندی بدون گفتگو", kind="update", feature="admin")
def mizito_admin_archive_category(
    project_id: ProjectId,
    undo: Annotated[bool, Field(description="true = restore a category archived earlier.")] = False,
) -> dict:
    """Archive (or restore) a project that has no project conversation (a web-app «دسته‌بندی»). Projects with a
    conversation are archived with mizito_archive_project."""
    call("projects.undoArchive" if undo else "projects.archive", {"project_id": project_id}, HINT)
    return {"project_id": project_id, "archived": not undo}

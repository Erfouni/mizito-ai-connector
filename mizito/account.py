"""Account and workspace: who am I, workspaces, members, dashboard, invitations, presence."""
from __future__ import annotations

from typing import Annotated

from pydantic import Field

from mizito.app import ADVANCED_PLAN_FEATURES, ToolError, call, check, client, compact, tool
from mizito_client import MizitoError


def _me() -> dict:
    return client.call("workspace.userId", {}) or {}


@tool("من کیستم / میزکار فعال")
def mizito_whoami() -> dict:
    """The logged-in Mizito user, the active workspace (میزکار) and the other workspaces this account can
    switch to, plus role, creation rights and the plan type: "basic" (پایه) or "advanced" (پیشرفته); advanced
    projects, Gantt, task templates, automation and advanced minutes exist only on the advanced plan. Call it
    first when you need your own user id (for example to assign a task to yourself) or to check whether you
    are a workspace admin or guest."""
    info = _me()
    return compact({
        "user_id": info.get("uid"),
        "user_name": client.user_name(info.get("uid")),
        "workspace_id": info.get("wid"),
        "workspaces": [
            {"id": w.get("_id"), "title": w.get("title"), "active": w.get("active")}
            for w in info.get("workspaces", [])
        ],
        "is_guest": info.get("is_guest"),
        "is_admin": info.get("access_admin"),
        "can_create_projects": info.get("access_project_creator"),
        "can_create_groups": info.get("access_chat_group_creator"),
        "can_create_crm_files": info.get("access_crm_creator"),
        "plan_type": "advanced" if info.get("is_enterprise_plan") is True else "basic",
        "plan_is_trial": info.get("plan_is_trial"),
        "plan_remaining_days": info.get("remain_days"),
    })


@tool("تغییر میزکار فعال", kind="set")
def mizito_switch_workspace(
    workspace_id: Annotated[str, Field(description="Workspace id from mizito_whoami's `workspaces`.")],
) -> dict:
    """Switch the active workspace. Every other tool then reads and acts on that workspace until you switch
    again. Returns the new mizito_whoami."""
    client.switch_workspace(workspace_id)
    return mizito_whoami()


@tool("داشبورد (شمارنده‌ها)")
def mizito_dashboard() -> dict:
    """Per-workspace counters from the Mizito dashboard: unread letters, unread chats, today's and overdue
    tasks and meetings. Good for a quick "what needs my attention" overview across workspaces."""
    return {"workspaces": compact(client.call("dashboard.getAllSummary", {}) or [])}


@tool("اعضای میزکار")
def mizito_list_users() -> dict:
    """Members of the active workspace: id, name, role (0 member, 1 admin, 2 guest), last seen, and whether
    they are only invited or removed. Use these ids for assignees, recipients, members and approvers."""
    data = client.call("workspace.getUsers", {}) or {}
    users = [
        compact({
            "id": u.get("_id"),
            "name": " ".join(p for p in (u.get("first_name"), u.get("last_name")) if p),
            "role": u.get("role"),
            "position": u.get("workspace_role_name"),
            "last_seen": (u.get("status") or {}).get("was_online"),
            "invited": u.get("invited"),
            "deleted": u.get("deleted"),
        })
        for u in data.get("users", [])
    ]
    return {"count": len(users), "users": users}


@tool("اطلاعات میزکار، پلن و دعوت‌ها")
def mizito_workspace_info() -> dict:
    """Workspace name, plan status (trial, remaining days, storage), your permissions, pending invitations
    from other workspaces (accept them with mizito_respond_workspace_invitation) and unread badges.
    Plan details (limits, invoices) are only visible to workspace admins."""
    info = _me()
    out = {
        "workspace_id": info.get("wid"),
        "name": client.call("workspace.name", {}),
        "plan": compact({
            "type": "advanced (پیشرفته)" if info.get("is_enterprise_plan") is True else "basic (پایه)",
            "advanced_plan_only": ADVANCED_PLAN_FEATURES,
            "trial": info.get("plan_is_trial"), "demo": info.get("plan_is_demo"),
            "remaining_days": info.get("remain_days"), "upgrade_needed": info.get("plan_upgrade_need"),
            "storage_almost_full": info.get("plan_storage_almost_full"),
        }),
        "permissions": compact({
            "admin": info.get("access_admin"), "guest": info.get("is_guest"),
            "create_projects": info.get("access_project_creator"),
            "create_groups": info.get("access_chat_group_creator"),
            "create_crm_files": info.get("access_crm_creator"),
            "workspace_role_names": info.get("access_workspace_role_names"),
        }),
        "pending_invitations": compact(client.call("dashboard.getPending", {}) or []),
        "badges": compact(client.call("dashboard.getAllBadges", {"only_badges": True}) or {}),
    }
    try:  # storage used / total, for every member
        out["plan"].update(compact({"storage": client.call("workspace.planInfo", {})}))
    except MizitoError:
        pass
    for key, endpoint, payload in (("plan_details", "workspace.planInfo", {"details": True}),
                                   ("member_permissions", "workspace.getPermissions", {})):
        try:
            out[key] = compact(client.call(endpoint, payload))
        except MizitoError:
            out[key] = "only visible to workspace admins"
    return compact(out)


@tool("پذیرش یا رد دعوت به میزکار دیگر", kind="set")
def mizito_respond_workspace_invitation(
    workspace_id: Annotated[str, Field(description="`workspace` of a pending invitation from mizito_workspace_info.")],
    accept: Annotated[bool, Field(description="true = join that workspace, false = decline the invitation.")],
) -> dict:
    """Accept or decline an invitation to join another Mizito workspace. After accepting, use
    mizito_switch_workspace to work in it. Only on the user's explicit request."""
    if accept:
        result = check(call("dashboard.acceptInviteRequest", {"workspace": workspace_id}), "accept the invitation")
    else:
        result = call("dashboard.cancelInviteRequest", {"workspace": workspace_id})
    return {"workspace_id": workspace_id, "accepted": accept, "result": compact(result)}


@tool("دعوت شخص جدید به میزکار", kind="create")
def mizito_invite_workspace_member(
    name: Annotated[str, Field(description="The person's full name.")],
    email_or_phone: Annotated[str, Field(description="Their email address or Iranian mobile number (09...).")],
    as_guest: Annotated[bool, Field(description="Invite as a guest (مهمان) who only sees what they are added to (advanced plans).")] = False,
) -> dict:
    """Invite someone without access to this workspace by email or mobile number; Mizito sends them the
    invitation. Afterwards add them to projects with mizito_add_project_members. May require workspace admin
    rights. Only on the user's explicit request."""
    result = call("workspace.inviteMember", {"name": name, "email_phone": email_or_phone, "is_guest": as_guest},
                  "inviting may need workspace admin rights or free seats in the plan")
    if isinstance(result, dict) and not result.get("success"):
        raise ToolError(f"Mizito did not send the invitation: {result.get('message') or result}")
    return {"invited": True, "result": compact(result)}


@tool("وضعیت حضور و مزاحم نشوید", kind="set")
def mizito_set_presence(
    status_text: Annotated[str | None, Field(description="Custom status shown next to your name (e.g. «در جلسه»); empty string clears it.")] = None,
    do_not_disturb_hours: Annotated[int | None, Field(description="Mute browser/app notifications for this many hours; 0 turns do-not-disturb off.", ge=0, le=720)] = None,
) -> dict:
    """Set your custom status text and/or do-not-disturb (مزاحم نشوید) period. Pass at least one."""
    if status_text is None and do_not_disturb_hours is None:
        return {"changed": False, "note": "Pass status_text and/or do_not_disturb_hours"}
    if status_text is not None:
        call("profile.setOnlineStatus", {"status": status_text})
    if do_not_disturb_hours is not None:
        call("profile.setDontDisturbUntil", {"hours": do_not_disturb_hours})
    return compact({"changed": True, "status_text": status_text, "do_not_disturb_hours": do_not_disturb_hours})

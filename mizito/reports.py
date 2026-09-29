"""Reports and monitoring (گزارش‌ها و مانیتورینگ): workspace, member, project and minutes statistics.
Mostly for workspace admins, or members given monitoring access to advanced projects."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mizito.app import ToolError, call, client, compact, iso, tool
from mizito_client import MizitoError

HINT = "reports need workspace admin rights (or monitoring access to the project) and a plan that includes them"

CHARTS = {
    "chart_chat_messages": "monitor.chart.chatMessages",
    "chart_letters": "monitor.chart.inboxMessages",
    "chart_notes": "monitor.chart.notes",
    "chart_customers": "monitor.chart.customers",
    "chart_tasks_created": "monitor.chart.tasksCreated",
    "chart_tasks_done": "monitor.chart.tasksDone",
    "chart_tasks_assigned": "monitor.chart.tasksAssigned",
}


def _first(endpoints: list[str], payload: dict):
    """Admins use monitor.*, project monitoring viewers the projects.monitor.* twins."""
    error = None
    for endpoint in endpoints:
        try:
            return client.call(endpoint, payload)
        except MizitoError as exc:
            error = exc
    raise ToolError(f"{error}. {HINT}")


@tool("گزارش‌ها و مانیتورینگ")
def mizito_reports(
    report: Annotated[Literal[
        "workspace", "member", "project", "projects_summary", "done_percent_30_days", "minutes", "customers",
        "chart_chat_messages", "chart_letters", "chart_notes", "chart_customers", "chart_tasks_created",
        "chart_tasks_done", "chart_tasks_assigned",
    ], Field(description=(
        "workspace = overall activity; member = one member's profile and workload (user_id); project = one project's "
        "health (project_id); projects_summary = every project's open/overdue/done tasks, longest delay and largest "
        "inbox; done_percent_30_days = share of tasks done on time over 30 days per project; minutes = meeting "
        "minutes matching filters; customers = CRM customer files; chart_* = daily counts (workspace, or one member "
        "with user_id)."))],
    user_id: Annotated[str | None, Field(description="Member for report=member or a chart_* for one member.")] = None,
    project_id: Annotated[str | None, Field(description="Project for report=project, or filter for minutes.")] = None,
    project_label_id: Annotated[str | None, Field(description="For projects_summary / done_percent_30_days: only projects with this label.")] = None,
    search: Annotated[str | None, Field(description="For minutes: text to search in the minutes.")] = None,
    from_date: Annotated[str | None, Field(description="For customers: created from (ISO or Jalali).")] = None,
    to_date: Annotated[str | None, Field(description="For customers: created until (ISO or Jalali).")] = None,
) -> dict:
    """Management reports from Mizito's monitoring section (مانیتورینگ). Useful for analysing workload,
    delays and activity. Needs workspace admin rights, or monitoring access to advanced projects."""
    if report == "workspace":
        data = call("monitor.workspace", {}, HINT)
    elif report == "member":
        if not user_id:
            raise ToolError("user_id is required for report=member")
        data = {"profile": call("monitor.user", {"uid": user_id}, HINT)}
        for key, endpoint, payload in (
            ("tasks_created", "monitor.chart.tasksCreated", {"uid": user_id}),
            ("tasks_done", "monitor.chart.tasksDone", {"uid": user_id}),
            ("tasks_assigned", "monitor.chart.tasksAssigned", {"uid": user_id}),
            ("tasks_assigned_by_others", "monitor.chart.tasksAssigned", {"uid": user_id, "not_owner": True}),
        ):
            try:
                data[key] = client.call(endpoint, payload)
            except MizitoError:
                pass
    elif report == "project":
        if not project_id:
            raise ToolError("project_id is required for report=project")
        data = _first(["monitor.project", "projects.monitor.project"], {"projectId": project_id})
    elif report in ("projects_summary", "done_percent_30_days"):
        payload = {"project_label": project_label_id} if project_label_id else {}
        if report == "projects_summary":
            data = _first(["monitor.projectsSummary", "projects.monitor.projectsSummary"], payload)
        else:
            data = _first(["monitor.chart.getPast30DoneTasksPercents", "projects.monitor.chart.getPast30DoneTasksPercents"], payload)
    elif report == "minutes":
        data = call("monitor.minutes", {"filter": {
            "member_owner": None, "member_executive": None, "member_observer": None, "member": user_id,
            "labels": [], "project": project_id, "content": search or "", "state": -1}}, HINT)
    elif report == "customers":
        data = call("monitor.customers", {"filter": {
            "access": user_id, "access_not": None, "created_by": None, "from_date": iso(from_date, default_time=(0, 0)),
            "to_date": iso(to_date, default_time=(23, 59)), "archive_status": 2}}, HINT)
    else:
        data = call(CHARTS[report], {"uid": user_id} if user_id else {}, HINT)
    return {"report": report, "data": _named(compact(data))}


def _named(value):
    """Add *_name next to user-id fields so reports read well."""
    if isinstance(value, list):
        return [_named(v) for v in value]
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            out[key] = _named(item)
            if key in ("user", "uid", "owner", "user_id", "member") and isinstance(item, str) and len(item) == 24:
                out[f"{key}_name"] = client.user_name(item)
        return out
    return value

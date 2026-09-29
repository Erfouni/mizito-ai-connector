"""Escape hatch: any read-only Mizito endpoint, for data no dedicated tool returns yet."""
from __future__ import annotations

import re
from typing import Annotated, Any

from pydantic import Field

from mizito.app import ToolError, client, compact, remember_files, remember_tasks, tool

_READ_METHOD = re.compile(
    r"^(get\w*|search\w*|history|info|upcoming|badge|allSummary|chatSummary|full|userInfo|userId|name|planInfo"
    r"|expandInboxRow|view|whatsNew|checkWhatsNew|loadSettings|loadConstants|ganttGetTaskInfo|ganttLoadMoreTasks"
    r"|suggestParticipants|clientOnlineHistory|getClientUnreadCount)$"
)
_BLOCKED_MODULES = {"session", "profile", "payment", "fix", "device", "feedback", "meeting"}
_REPORT_MODULES = {"monitor"}  # monitor.* are read-only statistics (monitor.workspace, monitor.chart.tasksDone, ...)


@tool("خواندن مستقیم از API میزیتو")
def mizito_api_read(
    endpoint: Annotated[str, Field(description='Endpoint "module.method", e.g. "chat.getMessageByDate", "labels.history", "monitor.workspace".')],
    payload: Annotated[dict[str, Any] | None, Field(description="JSON body, e.g. {\"dialog\": \"...\", \"date\": \"...\"}.")] = None,
) -> dict:
    """Call any read-only Mizito endpoint directly (get*/search*/history/info/view-style methods and monitor.*
    reports), for data the other tools do not cover. The full endpoint list with parameters is in the
    project's docs/site-map/api.md. Account, session, billing and admin-repair modules are blocked."""
    module, _, method = endpoint.rpartition(".")
    root = module.split(".")[0]
    if not module or root in _BLOCKED_MODULES or not (root in _REPORT_MODULES or _READ_METHOD.match(method)):
        raise ToolError(f"{endpoint!r} is not an allowed read-only endpoint")
    data = client.call(endpoint, payload or {})
    remember_files(data)
    if isinstance(data, list):
        remember_tasks(data)
    return {"endpoint": endpoint, "data": compact(data)}

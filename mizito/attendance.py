"""Attendance (حضور و غیاب): clock in/out and working-time history."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

from pydantic import Field

from mizito.app import ToolError, call, client, compact, jalali, tool

HINT = "attendance may be switched off for this workspace, or viewing others needs admin/monitoring rights"


def _parse(value) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


@tool("سابقه‌ی حضور و ساعات کار")
def mizito_attendance_history(
    kind: Annotated[Literal["online", "manual"], Field(description=(
        "online = time you were active in Mizito (automatic tracking); manual = the clock-in/clock-out records "
        "made with «اعلام حضور» / mizito_attendance."))] = "online",
    days: Annotated[int, Field(description="For online: how many recent days to cover.", ge=1, le=120)] = 14,
    user_id: Annotated[str | None, Field(description="Another member's history (workspace admins / monitoring access only).")] = None,
    offset: Annotated[int, Field(description="For manual: skip this many records (paging, 25 per page).", ge=0)] = 0,
) -> dict:
    """Working-time history (حضور و غیاب): sessions with start/end in Tehran time and daily totals in hours."""
    if kind == "online":
        end = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {"fromDate": (end - timedelta(days=days + 1)).isoformat().replace("+00:00", "Z"),
                   "toDate": end.isoformat().replace("+00:00", "Z")}
        if user_id:
            payload["userId"] = user_id
        data = call("monitor.attendanceUserOnlineHistory" if user_id else "attendance.getOnlineHistory", payload, HINT) or {}
        rows = data if isinstance(data, list) else data.get("rows") or []
    else:
        payload = {"fromIndex": offset}
        if user_id:
            payload["userId"] = user_id
        data = rows = call("monitor.attendanceUserHistory" if user_id else "attendance.getHistory", payload, HINT) or []
    sessions, per_day = [], defaultdict(float)
    for row in rows:
        start, stop = _parse(row.get("start_at")), _parse(row.get("stop_at"))
        hours = round(((stop - start).total_seconds() if start and stop else row.get("duration") or 0) / 3600, 2)
        day = jalali(start.isoformat())[:10] if start else None
        if day:
            per_day[day] += hours
        sessions.append(compact({"id": row.get("_id"), "start_jalali": jalali(row.get("start_at")),
                                 "end_jalali": jalali(row.get("stop_at")), "hours": hours,
                                 "open": not row.get("stop_at") or None}))
    return compact({
        "kind": kind, "user": client.user_name(user_id) if user_id else "me",
        "daily_hours": {day: round(h, 2) for day, h in sorted(per_day.items(), reverse=True)},
        "total_hours": round(sum(per_day.values()), 2),
        "sessions": sessions,
        "has_more": (data.get("has_more") if kind == "online" and isinstance(data, dict) else len(rows) == 25) or None,
    })


@tool("اعلام حضور / پایان حضور", kind="create")
def mizito_attendance(
    action: Annotated[Literal["start", "stop", "delete"], Field(description=(
        "start = clock in (اعلام حضور); stop = clock out (خاتمه حضور); delete = remove one manual record (record_id)."))],
    record_id: Annotated[str | None, Field(description="For delete: record id from mizito_attendance_history(kind='manual').")] = None,
) -> dict:
    """Clock in or out in Mizito's attendance (حضور و غیاب), or delete a wrong manual record. Only on the
    user's explicit request."""
    if action == "delete":
        if not record_id:
            raise ToolError("record_id is required for delete")
        call("attendance.delete", {"attendanceId": record_id}, HINT)
    else:
        call(f"attendance.{action}", {}, HINT)
    return {"action": action, "done": True, "at_jalali": jalali(datetime.now(timezone.utc).isoformat())}

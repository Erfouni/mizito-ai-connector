"""Gantt chart (گانت) of advanced projects: phases, task timelines and dependencies."""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from mizito.app import (
    WHEN_HELP, ProjectId, ToolError, call, client, compact, iso, jalali, load_task, names, project_full,
    remember_tasks, tool,
)

GANTT_HINT = ("the Gantt chart needs a project with advanced features and Gantt switched on "
              "(mizito_set_project_advanced features={'gantt': true}) and a plan that includes it")
NO_PHASE = 99999  # Mizito's bucket for Gantt tasks without a phase


def _gantt(project_id: str) -> tuple[dict, dict]:
    full = project_full(project_id)
    data = call("projects.getGanttData", {"project": project_id}, GANTT_HINT) or {}
    tasks = client.call("tasks.upcoming", {"project_id": project_id, "all": True, "from_gantt_view": True,
                                           "dialog": full.get("dialog"), "sort_type": "default", "from": 0,
                                           "filter": {"all_project_tasks": True, "done_status": False}}) or []
    by_id = {t["_id"]: t for t in tasks if isinstance(t, dict) and t.get("_id")}
    missing = [tid for g in data.get("groups") or [] for tid in g.get("task_ids") or [] if tid not in by_id]
    if missing:
        more = client.call("projects.ganttLoadMoreTasks", {"project": project_id, "taskIds": missing}) or []
        by_id.update({t["_id"]: t for t in more if isinstance(t, dict) and t.get("_id")})
    remember_tasks(list(by_id.values()))
    return data, by_id


@tool("نمودار گانت پروژه")
def mizito_get_gantt(project_id: ProjectId) -> dict:
    """The project's Gantt chart (گانت): phases (فاز) in order, each with its tasks' start and finish dates
    (Jalali too), progress and assignees, plus the dependencies between tasks (a task that must finish before
    another starts). Advanced projects with Gantt enabled only."""
    data, by_id = _gantt(project_id)
    depends: dict[str, list[str]] = {}
    for link in data.get("links") or []:
        depends.setdefault(link.get("to"), []).append(link.get("from"))
    phases = []
    for group in data.get("groups") or []:
        rows = []
        for tid in group.get("task_ids") or []:
            t = by_id.get(tid, {"_id": tid})
            rows.append(compact({
                "id": tid, "title": t.get("title"), "assignees": names(t.get("assignee")),
                "start": t.get("deadline_start"), "start_jalali": jalali(t.get("deadline_start")),
                "finish": t.get("deadline"), "finish_jalali": jalali(t.get("deadline")),
                "progress": t.get("progress"), "completed": t.get("completed"),
                "depends_on": [by_id.get(d, {}).get("title") or d for d in depends.get(tid, [])] or None,
                "depends_on_ids": depends.get(tid),
            }))
        phases.append(compact({
            "phase_id": group.get("_id"),
            "title": "(بدون فاز)" if group.get("_id") == NO_PHASE else group.get("title"),
            "tasks": rows,
        }))
    return {"project_id": project_id, "phases": phases,
            "links": [{"from": l.get("from"), "to": l.get("to")} for l in data.get("links") or []]}


@tool("ویرایش نمودار گانت (فاز، زمان‌بندی، وابستگی)", kind="update")
def mizito_manage_gantt(
    project_id: ProjectId,
    action: Annotated[Literal["add_phase", "rename_phase", "delete_phase", "add_tasks", "move_task", "remove_task",
                              "set_dates", "link", "unlink"], Field(description=(
        "add_phase (title, optional after_phase_id); rename_phase (phase_id, title); delete_phase (phase_id; its tasks "
        "leave the chart); add_tasks (task_ids, optional phase_id; default = no phase); move_task (task_id to "
        "to_phase_id, optional after_task_id); remove_task (task_id leaves the chart, the task stays); set_dates "
        "(task_id, start, finish); link (from_task_id must finish before to_task_id starts); unlink."))],
    phase_id: Annotated[int | str | None, Field(description="Phase id from mizito_get_gantt.")] = None,
    title: Annotated[str | None, Field(description="Phase name.")] = None,
    after_phase_id: Annotated[int | str | None, Field(description="For add_phase: put the new phase after this one (default: last).")] = None,
    task_ids: Annotated[list[str] | None, Field(description="For add_tasks: existing project task ids to put on the chart.")] = None,
    task_id: Annotated[str | None, Field(description="The task for move_task / remove_task / set_dates.")] = None,
    to_phase_id: Annotated[int | str | None, Field(description="For move_task: target phase id.")] = None,
    after_task_id: Annotated[str | None, Field(description="For move_task: place it after this task (default: first).")] = None,
    start: Annotated[str | None, Field(description="For set_dates: start. " + WHEN_HELP)] = None,
    finish: Annotated[str | None, Field(description="For set_dates: finish (becomes the task deadline). " + WHEN_HELP)] = None,
    from_task_id: Annotated[str | None, Field(description="For link/unlink: the task that must finish first.")] = None,
    to_task_id: Annotated[str | None, Field(description="For link/unlink: the task that waits for it.")] = None,
) -> dict:
    """Edit a project's Gantt chart: phases, which tasks are on it, their dates and dependencies. Changes are
    visible to everyone who can see the chart. Returns the updated chart."""
    data, by_id = _gantt(project_id)
    groups = [g for g in data.get("groups") or [] if g.get("_id") not in (NO_PHASE, -1)]

    def need(value, name):
        if value in (None, "", []):
            raise ToolError(f"{name} is required for {action}")
        return value

    if action == "add_phase":
        prev = after_phase_id if after_phase_id is not None else (groups[-1]["_id"] if groups else -1)
        call("projects.ganttSaveGroup", {"project": project_id, "phase": {"id": None, "title": need(title, "title"),
                                                                           "prevPhase": prev}}, GANTT_HINT)
    elif action == "rename_phase":
        ids = [g.get("_id") for g in groups]
        pid = need(phase_id, "phase_id")
        if pid not in ids:
            raise ToolError("Unknown phase_id (see mizito_get_gantt)")
        prev = ids[ids.index(pid) - 1] if ids.index(pid) > 0 else -1
        call("projects.ganttSaveGroup", {"project": project_id, "phase": {"id": pid, "title": need(title, "title"),
                                                                           "prevPhase": prev}}, GANTT_HINT)
    elif action == "delete_phase":
        call("projects.ganttRemoveGroup", {"project": project_id, "phaseId": need(phase_id, "phase_id")}, GANTT_HINT)
    elif action == "add_tasks":
        call("projects.ganttGroupAddTasks", {"project": project_id, "group": phase_id if phase_id is not None else NO_PHASE,
                                             "taskIds": need(task_ids, "task_ids")}, GANTT_HINT)
    elif action == "move_task":
        tid = need(task_id, "task_id")
        source = next((g.get("_id") for g in data.get("groups") or [] if tid in (g.get("task_ids") or [])), None)
        if source is None:
            raise ToolError("That task is not on the Gantt chart yet: use add_tasks first")
        call("projects.ganttMoveTask", {"project": project_id, "taskId": tid, "fromGroup": source,
                                        "toGroup": need(to_phase_id, "to_phase_id"), "afterTaskId": after_task_id}, GANTT_HINT)
    elif action == "remove_task":
        call("projects.ganttRemoveTask", {"project": project_id, "taskId": need(task_id, "task_id")}, GANTT_HINT)
    elif action == "set_dates":
        task = by_id.get(need(task_id, "task_id")) or load_task(task_id)
        call("projects.ganttSetTaskTimeline", {"project": project_id, "tasks": [{
            "_id": task_id, "start_date": iso(need(start, "start")), "finish_date": iso(need(finish, "finish")),
            "alarm_at": task.get("alarm_at")}]}, GANTT_HINT)
    else:
        endpoint = "projects.ganttTaskLinkAdd" if action == "link" else "projects.ganttTaskLinkRemove"
        call(endpoint, {"project": project_id, "fromTaskId": need(from_task_id, "from_task_id"),
                        "toTaskId": need(to_task_id, "to_task_id")}, GANTT_HINT)
    return {"action": action, "done": True, "gantt": mizito_get_gantt(project_id)}

"""Project automation (اتوماسیون) of advanced projects: rules, task buttons, custom fields, workflows and
request forms (فرم‌های درخواست)."""
from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import Field

from mizito.app import ProjectId, TaskId, ToolError, call, check, client, compact, load_task, remember_tasks, tool
from mizito_client import MizitoError

HINT = ("automation needs an advanced project with automation switched on (mizito_set_project_advanced "
        "features={'automation': true}), project admin rights for editing, and a plan that includes it")


@tool("اتوماسیون، فیلدهای سفارشی و گردش‌کار پروژه")
def mizito_get_project_automation(project_id: ProjectId) -> dict:
    """Everything automated in an advanced project: automation rules and buttons, custom task fields
    (پارامترهای سفارشی), workflows (گردش‌کار), request forms and task templates, plus the catalogue of rule
    condition/action types. Sections the project or plan does not have are omitted."""
    out: dict[str, Any] = {"project_id": project_id}
    for key, endpoint, payload in (
        ("rules", "projectAutomation.getAll", {"projectId": project_id}),
        ("custom_fields", "projectAutomation.customParam.getAll", {"projectId": project_id, "isAdminMode": True}),
        ("workflows", "projectAutomationWorkflow.getAll", {"projectId": project_id}),
        ("request_forms", "formRequestTemplate.getAll", {"projectId": project_id}),
        ("task_templates", "taskTemplates.getAll", {"projectId": project_id}),
        ("rule_types", "projectAutomation.loadConstants", {}),
    ):
        try:
            value = compact(client.call(endpoint, payload))
        except MizitoError:
            continue
        if value:
            out[key] = value
    if len(out) == 1:
        out["note"] = "No automation data is available: " + HINT
    return out


@tool("فرم‌های درخواست")
def mizito_list_request_forms(
    template_id: Annotated[str | None, Field(description="Show the fields of this form (to fill it with mizito_submit_request_form).")] = None,
) -> dict:
    """Request forms (فرم‌های درخواست) you can submit, e.g. leave or purchase requests. Each submission becomes
    a tracked task in the form's project. With template_id, shows that form's fields (param_id, title, type,
    required)."""
    if template_id:
        form = call("formRequestTemplate.view", {"templateId": template_id}, HINT) or {}
        return {"form": compact({k: v for k, v in form.items() if k != "form_access_token"})}
    return {"forms": compact(call("formRequestTemplate.getAllForms", {}, HINT) or [])}


@tool("ثبت فرم درخواست", kind="create")
def mizito_submit_request_form(
    template_id: Annotated[str, Field(description="Form id from mizito_list_request_forms.")],
    values: Annotated[dict[str, Any], Field(description="Field values keyed by param_id (see mizito_list_request_forms(template_id)); numbers for price fields.")],
) -> dict:
    """Submit a request form (ثبت درخواست). Returns the tracking code (شماره پیگیری); follow it under
    mizito_list_tasks(scope='following'). Only on the user's explicit request."""
    form = call("formRequestTemplate.view", {"templateId": template_id}, HINT) or {}
    missing = [p.get("title") or p.get("param_id") for p in form.get("params") or []
               if p.get("required") and values.get(p.get("param_id")) in (None, "")]
    if missing:
        raise ToolError(f"Required fields missing: {missing}")
    result = check(call("formRequestTemplate.submit", {"templateId": template_id, "custom_params_values": values}, HINT),
                   "submit the form")
    return {"submitted": True, "tracking_code": (result or {}).get("tracking_code"), "result": compact(result)}


@tool("اجرای دکمه‌ی اتوماسیون روی وظیفه", kind="update")
def mizito_run_task_automation(
    task_id: TaskId,
    button_id: Annotated[str, Field(description="Automation button id from mizito_get_task_extras(automation_buttons).")],
    custom_values: Annotated[dict[str, Any] | None, Field(description="Values for custom fields the button asks for, keyed by param_id.")] = None,
    selected_user_ids: Annotated[dict[str, list[str]] | None, Field(description="Users chosen for button actions that ask for people, keyed by the action id.")] = None,
) -> dict:
    """Press an automation button (دکمه اتوماسیون) on a task, e.g. «تأیید», «ارسال به مرحله بعد»: runs the
    project's automated actions (move board, assign, change fields, notify...). Only on the user's explicit
    request."""
    task = load_task(task_id)
    payload: dict[str, Any] = {"token": task["access_token"], "buttonId": button_id}
    if selected_user_ids:
        payload["selectedUserIds"] = selected_user_ids
    if custom_values:
        payload["customParams"] = custom_values
    check(call("projectAutomation.buttonClicked", payload, HINT), "run the automation")
    after = load_task(task_id)
    remember_tasks(after)
    return {"done": True, "task": compact({k: after.get(k) for k in ("_id", "title", "kanban_board", "assignee",
                                                                    "completed", "progress", "custom_params")})}


_EDIT = {
    ("rule", "create"): ("projectAutomation.add", "automateItem"),
    ("rule", "update"): ("projectAutomation.update", "automateItem"),
    ("rule", "delete"): ("projectAutomation.delete", "automateItemId"),
    ("custom_field", "create"): ("projectAutomation.customParam.add", "paramItem"),
    ("custom_field", "update"): ("projectAutomation.customParam.update", "paramItem"),
    ("custom_field", "delete"): ("projectAutomation.customParam.delete", "paramId"),
    ("custom_field", "restore"): ("projectAutomation.customParam.restore", "paramId"),
    ("workflow", "create"): ("projectAutomationWorkflow.add", "workflow"),
    ("workflow", "update"): ("projectAutomationWorkflow.update", "workflow"),
    ("workflow", "delete"): ("projectAutomationWorkflow.delete", "workflowId"),
    ("request_form", "create"): ("formRequestTemplate.add", "form"),
    ("request_form", "update"): ("formRequestTemplate.save", "form"),
    ("request_form", "delete"): ("formRequestTemplate.remove", "formId"),
}


@tool("ویرایش اتوماسیون پروژه (قوانین، فیلدها، گردش‌کار، فرم‌ها)", kind="update")
def mizito_manage_project_automation(
    project_id: ProjectId,
    kind: Annotated[Literal["rule", "custom_field", "workflow", "request_form"], Field(description=(
        "rule = automation rule or button; custom_field = custom task field; workflow = multi-step workflow; "
        "request_form = request form template."))],
    action: Annotated[Literal["create", "update", "delete", "restore", "reorder"], Field(description=(
        "create / update (item) / delete (item_id) / restore a deleted custom field (item_id) / reorder custom "
        "fields (order_ids)."))],
    item: Annotated[dict[str, Any] | None, Field(description=(
        "For create/update: the object in the same shape mizito_get_project_automation returns (keep `_id` for "
        "update). Rules use condition/action types from its rule_types."))] = None,
    item_id: Annotated[str | None, Field(description="For delete/restore: the rule/field/workflow/form id.")] = None,
    order_ids: Annotated[list[str] | None, Field(description="For reorder: custom field ids in the new order.")] = None,
) -> dict:
    """Create, change or delete a project's automation rules, custom fields, workflows and request forms,
    the same objects the web app's automation editor saves. Needs project admin rights in an advanced project.
    Read the current objects with mizito_get_project_automation first."""
    base = {"projectId": project_id}
    if action == "reorder":
        if kind != "custom_field" or not order_ids:
            raise ToolError("reorder applies to custom fields and needs order_ids")
        result = call("projectAutomation.customParam.updateOrder", {**base, "items": order_ids}, HINT)
        return {"done": True, "result": compact(result)}
    spec = _EDIT.get((kind, action))
    if not spec:
        raise ToolError(f"{action} is not available for {kind}")
    endpoint, key = spec
    if key.endswith("Id"):
        if not item_id:
            raise ToolError("item_id is required")
        result = call(endpoint, {**base, key: item_id}, HINT)
    else:
        if not item:
            raise ToolError("item is required")
        payload = {**base, key: item}
        if kind == "custom_field" and action == "update":
            payload["paramId"] = item.get("_id") or item_id
        result = call(endpoint, payload, HINT)
    return {"done": True, "kind": kind, "action": action, "result": compact(check(result, f"{action} the {kind}"))}

"""Creation contracts, using real tools and client with an in-memory HTTP boundary.

Run: uv run python tests/test_creation.py. No account or network is needed.
"""
import asyncio
import copy
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["MIZITO_ENABLE_WRITE"] = "1"

from mizito import app, projects, tasks  # noqa: E402


class CreationTests(unittest.TestCase):
    def setUp(self):
        self.project = {"_id": "p1", "title": "Verified project", "dialog": "d1", "owner": "me",
                        "members": ["me", "other"], "color": "grey", "archived": False}
        self.visible = True
        self.saved = {}
        self.requests = []
        self.add_reply = None
        self.use_add_reply = False
        self.ignore_fields = set()
        self.copies = 1
        self.get_fails = False
        self.snooze_fails = False
        self.saved_overrides = {}
        self.project_reply = {"_id": "d1", "project_entity": "p1"}
        self.add_timeout = False
        self.read_overrides = {}
        self.transport = httpx.Client(transport=httpx.MockTransport(self.api))
        self.addCleanup(self.transport.close)
        for name, value in (("_http", self.transport), ("token", "offline-test-token"),
                            ("_my_id", None), ("_users", None), ("_username", None), ("_password", None)):
            p = patch.object(app.client, name, value)
            p.start()
            self.addCleanup(p.stop)
        p = patch.dict(app._task_tokens, {}, clear=True)
        p.start()
        self.addCleanup(p.stop)

    def api(self, request):
        endpoint = request.url.path.removeprefix("/api/").replace("/", ".")
        body = json.loads(request.content)
        self.requests.append((endpoint, body))
        if endpoint == "workspace.userId":
            data = {"uid": "me", "wid": "w1"}
        elif endpoint == "workspace.getUsers":
            data = {"users": [{"_id": "me", "first_name": "Owner"}, {"_id": "other", "first_name": "Colleague"}]}
        elif endpoint == "projects.full":
            data = self.project
        elif endpoint == "projects.getList":
            data = {"projects": [self.project]}
        elif endpoint == "projects.allSummary":
            data = {"summaries": [{"project": "p1", "dialog": "d1"}] if self.visible else []}
        elif endpoint == "chat.createDialog":
            data = self.project_reply
        elif endpoint == "tasks.add":
            if self.add_timeout:
                raise httpx.ReadTimeout("simulated unknown write outcome", request=request)
            if self.use_add_reply:
                data = self.add_reply
            else:
                data = []
                for index in range(self.copies):
                    tid = f"t{index + 1}"
                    row = {**copy.deepcopy(body), "_id": tid, "access_token": f"task-token-{tid}",
                           "completed": False}
                    if body.get("copy_users"):
                        row["assignee"] = [body["copy_users"][index]]
                    if row.get("alarm_options"):
                        row["alarm_at"] = row["alarm_options"]["date"]
                    self.saved[tid] = copy.deepcopy(row)
                    for field in self.ignore_fields:
                        self.saved[tid].pop(field, None)
                    self.saved[tid].update(self.saved_overrides)
                    data.append(row)
        elif endpoint == "tasks.get":
            if self.get_fails:
                return httpx.Response(400, json={"error": "not readable"})
            data = self.saved.get(body["token"].removeprefix("task-token-"), {})
        elif endpoint == "tasks.upcoming":
            data = list(self.saved.values()) if not self.get_fails else []
        elif endpoint == "tasks.snooze":
            if self.snooze_fails:
                data = False
            else:
                self.saved[body["token"].removeprefix("task-token-")]["alarm_at"] = body["alarm_at"]
                data = True
        elif endpoint == "taskTemplates.getAllTemplates":
            data = [{"_id": "tpl", "assignee_default": ["other"]}]
        else:
            raise AssertionError(f"Unexpected API request: {endpoint}")
        return httpx.Response(200, json=self.read_overrides.get(endpoint, data))

    def create(self, **kwargs):
        return tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=["me"], **kwargs)

    def assert_no_task_write(self):
        self.assertFalse(any(endpoint == "tasks.add" for endpoint, _ in self.requests))

    def test_empty_assignees_default_to_current_project_member(self):
        result = tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=[])
        self.assertEqual(self.saved["t1"]["assignee"], ["me"])
        self.assertEqual(result["created"], 1)
        self.assertTrue(result["verified"])

    def test_mcp_schema_allows_omitted_assignees(self):
        result = asyncio.run(app.mcp.call_tool("mizito_create_task", {"title": "Verify task", "project_id": "p1"}))
        self.assertTrue(result.structured_content["verified"])
        self.assertEqual(self.saved["t1"]["assignee"], ["me"])

    def test_default_does_not_assign_nonmember(self):
        self.project["members"] = ["other"]
        with self.assertRaises(app.ToolError):
            tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=[])
        self.assert_no_task_write()

    def test_explicit_invalid_assignee_is_rejected_before_write(self):
        with self.assertRaises(app.ToolError):
            tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=["outsider"])
        self.assert_no_task_write()

    def test_template_assignee_takes_precedence_over_self_default(self):
        result = tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=[], template_id="tpl")
        self.assertEqual(self.saved["t1"]["assignee"], ["other"])
        self.assertEqual(result["created"], 1)

    def test_unusable_add_responses_never_claim_success(self):
        self.use_add_reply = True
        for reply in (None, True, False, {}, [], {"success": True}, {"title": "no id"},
                      [{"_id": "t1"}, {"error": "second failed"}]):
            with self.subTest(reply=reply):
                self.add_reply = reply
                with self.assertRaises(app.ToolError):
                    self.create()

    def test_response_is_not_proof_of_persisted_fields(self):
        for field, kwargs in (("title", {}), ("project", {}), ("assignee", {}),
                              ("deadline", {"deadline": "1405/07/20 09:00"}),
                              ("notes", {"notes": "Expected description"}),
                              ("checklist", {"checklist": ["Check A"]})):
            with self.subTest(field=field):
                self.ignore_fields = {field}
                with self.assertRaisesRegex(app.ToolError, "t1"):
                    self.create(**kwargs)

    def test_read_failure_reports_known_id_without_recreating_task(self):
        self.get_fails = True
        with self.assertRaisesRegex(app.ToolError, "t1"):
            self.create()
        self.assertEqual(sum(ep == "tasks.add" for ep, _ in self.requests), 1)

    def test_success_requires_independent_read_and_returns_ids(self):
        result = self.create(deadline="1405/07/20 09:00", checklist=["Check A"])
        self.assertEqual(result["created"], 1)
        self.assertTrue(result["verified"])
        self.assertEqual(result["tasks"][0]["id"], "t1")
        self.assertEqual(result["tasks"][0]["deadline"], "2026-10-12T05:30:00.000Z")
        self.assertTrue(any(ep == "tasks.get" for ep, _ in self.requests))
        self.assertNotIn("task-token", json.dumps(result))

    def test_partial_copy_creation_is_an_error_with_recovery_ids(self):
        with self.assertRaisesRegex(app.ToolError, "t1"):
            tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=["me", "other"],
                                     one_copy_per_assignee=True)
        self.assertEqual(len(self.saved), 1)

    def test_all_copies_must_have_the_requested_assignees(self):
        self.copies = 2
        result = tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=["me", "other"],
                                          one_copy_per_assignee=True)
        self.assertTrue(result["verified"])
        self.assertEqual(result["created"], 2)

    def test_two_copies_for_same_person_do_not_satisfy_two_requested_assignees(self):
        self.copies = 2
        self.saved_overrides = {"assignee": ["me"]}
        with self.assertRaises(app.ToolError):
            tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=["me", "other"],
                                     one_copy_per_assignee=True)

    def test_write_timeout_is_uncertain_and_is_not_retried(self):
        self.add_timeout = True
        with self.assertRaisesRegex(app.ToolError, "NOT verified"):
            self.create()
        self.assertEqual(sum(ep == "tasks.add" for ep, _ in self.requests), 1)

    def test_error_body_preserves_candidate_task_id(self):
        self.use_add_reply = True
        self.add_reply = {"_id": "t-known", "success": False, "error": "partial"}
        with self.assertRaisesRegex(app.ToolError, "t-known"):
            self.create()

    def test_malformed_read_keeps_task_recovery_ids(self):
        for response in (True, {"_id": "t1", "access_token": "task-token-t1", "assignee": [123]}):
            with self.subTest(response=response):
                self.read_overrides = {"tasks.get": response}
                with self.assertRaisesRegex(app.ToolError, "Candidate task ids:.*t1"):
                    self.create()

    def test_malformed_project_read_keeps_project_recovery_id(self):
        self.read_overrides = {"projects.allSummary": True}
        with self.assertRaisesRegex(app.ToolError, "Candidate project ids:.*p1"):
            projects.mizito_create_project("Verified project")

    def test_unrequested_repeat_is_not_verified(self):
        self.saved_overrides = {"alarm_options": {"repeat_type": "daily"}}
        with self.assertRaisesRegex(app.ToolError, "t1"):
            self.create(remind_at="1405/07/20 09:00")

    def test_successful_reminder_repair_is_read_back(self):
        self.ignore_fields = {"alarm_at"}
        result = self.create(remind_at="1405/07/20 09:00")
        self.assertTrue(result["verified"])
        self.assertEqual(result["tasks"][0]["reminder"], "2026-10-12T05:30:00.000Z")
        self.assertEqual(sum(ep == "tasks.get" for ep, _ in self.requests), 2)

    def test_duplicate_task_ids_are_not_two_copies(self):
        self.use_add_reply = True
        self.add_reply = [{"_id": "t1"}, {"_id": "t1"}]
        with self.assertRaisesRegex(app.ToolError, "t1"):
            tasks.mizito_create_task(title="Verify task", project_id="p1", assignee_ids=["me", "other"],
                                     one_copy_per_assignee=True)

    def test_deleted_task_cannot_count_as_success(self):
        self.saved_overrides = {"deleted": True}
        with self.assertRaisesRegex(app.ToolError, "t1"):
            self.create()

    def test_basic_plan_may_omit_weight_when_user_did_not_request_it(self):
        # Observed on the real basic-plan account: tasks.add sends the web default 1,
        # but tasks.get returns weight=null. An explicit requested weight must still match.
        self.saved_overrides = {"weight": None}
        result = self.create()
        self.assertTrue(result["verified"])

    def test_optional_fields_cannot_be_silently_dropped(self):
        for field, kwargs in (("deadline_start", {"start": "1405/07/20 09:00"}),
                              ("kanban_board", {"board_id": "b1"}), ("labels", {"label_ids": ["label1"]}),
                              ("weight", {"weight": 3}), ("alarm_options", {
                                  "remind_at": "1405/07/20 09:00", "repeat": "weekly", "repeat_weekdays": ["sat"]})):
            with self.subTest(field=field):
                self.ignore_fields = {field}
                with self.assertRaisesRegex(app.ToolError, "t1"):
                    self.create(**kwargs)

    def test_missing_project_conversation_preserves_returned_project_id(self):
        self.project_reply = {"project_entity": "p1"}
        with self.assertRaisesRegex(app.ToolError, "p1"):
            projects.mizito_create_project("Verified project")

    def test_missing_requested_project_member_is_not_success(self):
        self.project["members"] = ["me"]
        with self.assertRaisesRegex(app.ToolError, "p1"):
            projects.mizito_create_project("Verified project", member_ids=["other"])

    def test_ignored_reminder_does_not_claim_complete_success(self):
        self.ignore_fields = {"alarm_at"}
        self.snooze_fails = True
        with self.assertRaisesRegex(app.ToolError, "t1"):
            self.create(remind_at="1405/07/20 09:00")

    def test_project_missing_from_list_is_not_success(self):
        self.visible = False
        with self.assertRaisesRegex(app.ToolError, "p1"):
            projects.mizito_create_project("Verified project")

    def test_project_missing_conversation_or_member_is_not_success(self):
        for field, value in (("dialog", None), ("dialog", "different-dialog"),
                             ("members", ["other"]), ("archived", True), ("title", "Wrong title")):
            with self.subTest(field=field):
                original = self.project[field]
                self.project[field] = value
                with self.assertRaises(app.ToolError):
                    projects.mizito_create_project("Verified project")
                self.project[field] = original

    def test_project_success_is_verified(self):
        result = projects.mizito_create_project("Verified project", member_ids=["other"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["project_id"], "p1")
        self.assertTrue(result["project"]["in_projects_tab"])


if __name__ == "__main__":
    unittest.main()

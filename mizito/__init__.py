"""Mizito MCP tools. `mizito.app` holds the shared client and MCP server; every other module
registers one area of tools (chat, tasks, letters, ...) when it is imported."""

MODULES = (
    "account", "chat", "meetings", "projects", "tasks", "gantt", "letters", "notes",
    "files", "attendance", "reports", "automation", "crm", "admin", "support", "raw",
)

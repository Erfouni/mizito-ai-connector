"""MCP server that exposes a Mizito (office.mizito.ir) workspace to Claude / ChatGPT.

Run locally over stdio (Claude Desktop / Claude Code):   uv run server.py
Run as a remote HTTP server (Claude.ai / ChatGPT):       MCP_TRANSPORT=streamable-http uv run server.py

The tools live in the mizito/ package, one module per area (chat, tasks, letters, ...);
docs/TOOLS.md describes every tool.
"""
from __future__ import annotations

import importlib
import os

from mcp.server.transport_security import TransportSecuritySettings

import mizito
from mizito.app import mcp

for _module in mizito.MODULES:  # importing a module registers its tools
    importlib.import_module(f"mizito.{_module}")


def _transport_security() -> TransportSecuritySettings | None:
    """Behind a reverse proxy the Host header is the public name, which the SDK's
    localhost-only default would reject; allow it explicitly via MCP_PUBLIC_HOST."""
    public_host = os.getenv("MCP_PUBLIC_HOST")
    if not public_host:
        return None
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[public_host, "127.0.0.1:*", "localhost:*"],
        allowed_origins=[f"https://{public_host}", "https://claude.ai", "https://chatgpt.com", "https://chat.openai.com"],
    )


if __name__ == "__main__":
    if os.getenv("MCP_TRANSPORT", "stdio") == "streamable-http":
        import uvicorn

        host = os.getenv("MCP_HOST", "127.0.0.1")
        app = mcp.streamable_http_app(
            streamable_http_path=os.getenv("MCP_HTTP_PATH", "/mcp"),
            # Tools keep no per-session state, so stateless JSON responses survive
            # restarts and proxies better than long-lived SSE sessions.
            stateless_http=True,
            json_response=True,
            transport_security=_transport_security(),
            host=host,
        )
        # Run uvicorn directly to switch its access log off: the URL path is the connector's secret.
        uvicorn.run(app, host=host, port=int(os.getenv("MCP_PORT", "8000")), access_log=False, log_level="info")
    else:
        mcp.run()

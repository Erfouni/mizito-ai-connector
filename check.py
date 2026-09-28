"""End-to-end check: starts server.py over stdio like Claude Desktop would, lists tools,
then calls the read-only tools and prints only a short summary of each result."""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).parent

# Persian text would crash a cp1252 stdout when output is piped on Windows.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def payload(result):
    """Tool data: structured content if the server sent it, else the JSON text block."""
    data = result.structured_content
    if data is None and result.content and hasattr(result.content[0], "text"):
        try:
            data = json.loads(result.content[0].text)
        except ValueError:
            data = result.content[0].text
    if isinstance(data, dict) and set(data) == {"result"}:
        data = data["result"]
    return data


def summarize(result) -> str:
    if result.is_error:
        return "ERROR: " + " ".join(c.text for c in result.content if hasattr(c, "text"))[:300]
    data = payload(result)
    if isinstance(data, list):
        return f"list[{len(data)}]" + (f" keys={sorted(data[0])[:8]}" if data and isinstance(data[0], dict) else "")
    if isinstance(data, dict):
        lists = {k: len(v) for k, v in data.items() if isinstance(v, list)}
        return "dict keys=" + str(sorted(data)[:10]) + (f" list sizes={lists}" if lists else "")
    return type(data).__name__


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")], cwd=str(HERE))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            print(f"{len(tools)} tools:", ", ".join(t.name for t in tools))

            whoami = await session.call_tool("mizito_whoami", {})
            print("mizito_whoami ->", summarize(whoami))
            if whoami.is_error:
                return

            convs = await session.call_tool("mizito_list_conversations", {})
            print("mizito_list_conversations ->", summarize(convs))
            for name, args in [
                ("mizito_dashboard", {}),
                ("mizito_list_users", {}),
                ("mizito_search_messages", {"query": "سلام"}),
                ("mizito_list_projects", {}),
                ("mizito_list_tasks", {"scope": "mine"}),
                ("mizito_list_tasks", {"scope": "following"}),
                ("mizito_list_letters", {"box": "inbox"}),
                ("mizito_list_notes", {}),
                ("mizito_api_read", {"endpoint": "labels.getAll", "payload": {"type": "task"}}),
            ]:
                print(f"{name}({json.dumps(args, ensure_ascii=False)}) ->", summarize(await session.call_tool(name, args)))

            conv_list = (payload(convs) or {}).get("conversations") or []
            if conv_list:
                biggest = max(conv_list, key=lambda c: c.get("messages_count") or 0)
                msgs = await session.call_tool("mizito_get_messages", {"conversation_id": biggest["id"], "count": 40})
                data = payload(msgs) or {}
                print(
                    "mizito_get_messages ->", summarize(msgs),
                    f"returned={data.get('returned')} of {data.get('messages_count')}, next_offset={data.get('next_offset')}",
                )


if __name__ == "__main__":
    asyncio.run(main())

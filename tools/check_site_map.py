"""Completeness check for docs/site-map: every state, view, endpoint and MCP call must be in the docs."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "site-map"
data = json.loads((DOCS / "site_map.json").read_text(encoding="utf-8"))
pages = (DOCS / "pages.md").read_text(encoding="utf-8")
views = (DOCS / "views.md").read_text(encoding="utf-8")
api = (DOCS / "api.md").read_text(encoding="utf-8")
rt = (DOCS / "realtime-and-types.md").read_text(encoding="utf-8")
server = (ROOT / "server.py").read_text(encoding="utf-8")

problems = []
for s in data["states"]:
    if f"### `{s['name']}`" not in pages:
        problems.append(f"state missing from pages.md: {s['name']}")
for name in data["views"]:
    if f"### `{name}`" not in views:
        problems.append(f"view missing from views.md: {name}")
for ep in data["endpoints"]:
    if f"| `{ep}` |" not in api:
        problems.append(f"endpoint missing from api.md: {ep}")
for ep in set(re.findall(r"client\.(?:call|_post)\(\s*\"([\w.]+)\"", server)):
    if ep not in data["endpoints"]:
        problems.append(f"endpoint used by server.py but not found in the web client: {ep}")
for key in ("message_media_types", "message_action_types", "plan_options", "access_flags", "local_storage"):
    for item in data[key]:
        if f"`{item}`" not in rt:
            problems.append(f"{key} item missing from realtime-and-types.md: {item}")
for ev in data["realtime"]["out_workspace_events"] + data["realtime"]["listened_not_broadcast"]:
    if f"`{ev}`" not in rt:
        problems.append(f"realtime event missing: {ev}")

counts = {
    "states": (len(data["states"]), pages.count("### `")),
    "views": (len(data["views"]), views.count("### `")),
    "endpoints": (len(data["endpoints"]), len(re.findall(r"^\| `[\w.]+` \|", api, flags=re.M))),
}
print("counts (data, docs):", counts)
print("problems:", len(problems))
for p in problems[:50]:
    print("  -", p)
sys.exit(1 if problems else 0)

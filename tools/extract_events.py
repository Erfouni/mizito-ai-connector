"""Leftovers for the Mizito map: states defined another way, server-pushed event types, print view.
Writes /tmp/mizito_events.json."""
import json
import re
import urllib.request

T = open("/tmp/mizito_a.js", encoding="utf-8", errors="replace").read()
PERSIAN = re.compile(r"(?:\\u[0-9A-Fa-f]{4})+")
out = {}

# states registered with a different call shape (e.g. delete_account.*)
out["other_state_defs"] = [PERSIAN.sub("·", T[max(0, m.start() - 120):m.start() + 260])
                           for m in re.finditer(r"[\"']delete_account[\"'.]", T)][:6]
out["all_state_names"] = sorted(set(re.findall(r"\.state\([\"']([a-z_.]+)[\"']", T))
                                | set(re.findall(r"name:\"((?:delete_account|login|register|ws)[a-z_.]*)\",url", T)))

# every $scope/$rootScope event handler name; server pushes arrive as $broadcast(type) or "out_workspace_" + type
on_names = re.findall(r"\$on\(\"([A-Za-z0-9_:.\-]+)\"", T)
out["on_event_counts"] = {n: on_names.count(n) for n in sorted(set(on_names))}
out["out_workspace_events"] = sorted({n[len("out_workspace_"):] for n in on_names if n.startswith("out_workspace_")})
broadcast_names = set(re.findall(r"\$broadcast\(\"([A-Za-z0-9_:.\-]+)\"", T))
# names that are listened to but never broadcast by the client itself come from the server socket
out["server_pushed_candidates"] = sorted(set(on_names) - broadcast_names)
out["socket_type_checks"] = sorted(set(re.findall(r"\.type==\"([a-z_]+)\"|\"([a-z_]+)\"==\w\.type", T)) - {("", "")})

# the one view that did not download
try:
    with urllib.request.urlopen(urllib.request.Request("https://office.mizito.ir/views/print/print-content.html",
                                                       headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r:
        out["print_view"] = {"status": r.status, "size": len(r.read())}
except Exception as exc:  # noqa: BLE001
    out["print_view"] = {"error": repr(exc)[:200]}

json.dump(out, open("/tmp/mizito_events.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (len(v) if hasattr(v, "__len__") else v) for k, v in out.items()})

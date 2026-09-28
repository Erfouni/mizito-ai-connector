"""Realtime (socket.io) handling, settings sub-pages and other dynamic UI names in the Mizito bundle.
Writes /tmp/mizito_extra.json."""
import json
import re

T = open("/tmp/mizito_a.js", encoding="utf-8", errors="replace").read()
PERSIAN = re.compile(r"(?:\\u[0-9A-Fa-f]{4})+")


def ctx(pos, before, after):
    return PERSIAN.sub("·", T[max(0, pos - before):pos + after])


out = {}

# socket.io connection and events
io_sites = [m.start() for m in re.finditer(r"\bio\(|io\.connect\(", T)]
out["io_contexts"] = [ctx(p, 300, 1500) for p in io_sites]
sock_events = set()
for p in io_sites:
    seg = T[p:p + 20000]
    sock_events |= set(re.findall(r"\.on\(\"([A-Za-z_:.\-]+)\"", seg))
    sock_events |= set(re.findall(r"\.emit\(\"([A-Za-z_:.\-]+)\"", seg))
out["socket_events_near_io"] = sorted(sock_events)

# update types dispatched from realtime payloads ({_: "updateXxx"} style) and case labels
out["update_types"] = sorted(set(re.findall(r"[\"'](update[A-Z]\w+)[\"']", T)))
out["case_labels"] = sorted(set(re.findall(r"case\"([A-Za-z_][\w:.]*)\":", T)))
out["media_types"] = sorted(set(re.findall(r"[\"'](messageMedia\w+)[\"']", T)))
out["action_types"] = sorted(set(re.findall(r"[\"'](messageAction\w+)[\"']", T)))

# settings sub-pages and other state params used in $state.go / ui-sref
out["settings_pages"] = sorted(set(re.findall(r"\"ws\.settings(?:_mobile)?\",\{page:\"([^\"]+)\"", T))
                               | set(re.findall(r"ws\.settings(?:_mobile)?\(\{page:'([^']+)'\}\)", T)))
out["state_go_targets"] = sorted(set(re.findall(r"\.go\(\"([a-z_.]+)\"", T)))
out["settings_ctx"] = [ctx(m.start(), 200, 600) for m in re.finditer(r"\"ws\.settings\",\{url", T)][:1]

# templates referenced through variables: collect string literals that look like view paths
tpl_like = set(re.findall(r"\"((?:partial|chat|tasks|projects|crm|sales|inbox|notes|workspace|settings|monitoring|meeting|minute|minutes|polling|support|search|login|home|print|profile|task|calendar|attendance|form_request|formrequest|automation|fix|labels|payment|payments|deal|deals|customer|customers|reports?)/[a-z0-9_\-/]+)\"", T))
out["template_like_strings"] = sorted(tpl_like)

# user-visible feature switches in workspace settings / plan
out["workspace_settings_keys"] = sorted(set(re.findall(r"setWorkspaceSettings\",\{([^}]{0,300})\}", T)))
out["options_keys"] = sorted(set(re.findall(r"setUserOptions\",\{([^}]{0,200})\}", T)))

json.dump(out, open("/tmp/mizito_extra.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in out.items()})

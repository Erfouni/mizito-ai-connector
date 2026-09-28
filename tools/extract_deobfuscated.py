"""Find what the obfuscated half of the bundle hides, using webcrack's output (deobfuscated.js).
usage: python tools/extract_deobfuscated.py <deobfuscated.js> <mizito_map.json> <mizito_templates.json> <out.json>"""
import html
import json
import re
import sys

src, map_path, views_path, out_path = sys.argv[1:5]
T = open(src, encoding="utf-8", errors="replace").read()
MAP = json.load(open(map_path, encoding="utf-8"))
VIEWS = json.load(open(views_path, encoding="utf-8"))
known = set(MAP["endpoints"])
mods = sorted({e.split(".")[0] for e in known})


def module_before(pos):
    found = list(re.finditer(r"\.(service|factory|controller|directive|filter|component|provider)\(\s*\"([^\"]+)\"", T[max(0, pos - 400000):pos]))
    return f"{found[-1].group(1)}:{found[-1].group(2)}" if found else "(top-level)"


def payload_keys(pos):
    j = pos
    while j < len(T) and T[j] in " \n\t,":
        j += 1
    if j >= len(T) or T[j] != "{":
        v = re.match(r"[\w$.]+", T[j:j + 40])
        return "var:" + (v.group(0) if v else "?")
    depth, k = 0, j
    while k < len(T) and k < j + 6000:
        depth += {"{": 1, "}": -1}.get(T[k], 0)
        if depth == 0:
            break
        k += 1
    body = T[j + 1:k]
    for _ in range(4):
        body = re.sub(r"\{[^{}]*\}|\[[^\[\]]*\]|\([^()]*\)", "~", body)
    return ",".join(re.findall(r"(?:^|,)\s*\"?([A-Za-z_$][\w$]*)\"?\s*:", body)) or "{}"


# endpoints: literal first argument of invokeApi (any spacing), wrappers and ternaries
found = {}
for m in re.finditer(r"invokeApi\(\s*", T):
    i, depth, arg = m.end(), 0, []
    while i < len(T) and i < m.end() + 600:
        ch = T[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            if depth == 0:
                break
            depth -= 1
        elif ch == "," and depth == 0:
            break
        arg.append(ch)
        i += 1
    for name in re.findall(r"\"([A-Za-z][A-Za-z0-9_]*\.[A-Za-z0-9_.]+)\"", "".join(arg)):
        found.setdefault(name, {"params": set(), "modules": set()})
        found[name]["params"].add(payload_keys(i) if i < len(T) and T[i] == "," else "-")
        found[name]["modules"].add(module_before(m.start()))
INDIRECT = re.compile(r"(\$watch\(\s*|[(?:]\s*)\"((?:" + "|".join(mods) + r")\.[a-z][A-Za-z]{2,}(?:\.[a-z][A-Za-z]{2,})*)\"(?=\s*([),:]))")
for m in INDIRECT.finditer(T):
    if m.group(1).startswith("$watch"):
        continue
    name = m.group(2)
    found.setdefault(name, {"params": set(), "modules": set()})
    found[name]["params"].add(payload_keys(m.end()) if m.group(3) == "," else "-")
    found[name]["modules"].add(module_before(m.start()))
new_endpoints = {k: {"params": sorted(v["params"]), "modules": sorted(v["modules"])} for k, v in found.items() if k not in known}

# states and view references that only exist in the (formerly) obfuscated code
states = set(re.findall(r"\.state\(\s*\"([^\"]+)\"", T))
new_states = sorted(states - {s["name"] for s in MAP["states"]})
view_refs = set(re.findall(r"templateUrl\(\s*\"([^\"]+)\"\s*\)", T))
new_views = sorted(view_refs - set(VIEWS))

# inline HTML templates (directive/component `template:` strings and html built in code)
inline = []
for m in re.finditer(r"template\s*:\s*(\"(?:[^\"\\]|\\.){40,}\"|`[^`]{40,}`)", T):
    raw = m.group(1)
    try:
        body = json.loads(raw) if raw.startswith("\"") else raw[1:-1]
    except Exception:
        body = raw[1:-1]
    if "<" not in body:
        continue
    texts = sorted({html.unescape(t).strip() for t in re.split(r"<[^>]+>|\{\{.*?\}\}", body)
                    if re.search(r"[؀-ۿ]", t) and len(t.strip()) < 120})
    inline.append({
        "owner": module_before(m.start()),
        "size": len(body),
        "texts": texts[:40],
        "clicks": sorted({re.split(r"[(\s]", c)[0] for c in re.findall(r"ng-click=\"([^\"]+)\"", body)}),
        "models": sorted(set(re.findall(r"ng-model=\"([^\"]+)\"", body))),
        "srefs": sorted(set(re.findall(r"ui-sref=\"([^\"]+)\"", body))),
        "includes": sorted(set(re.findall(r"templateUrl\('([^']+)'\)", body))),
    })

socket_types = sorted(set(re.findall(r"\$on\(\s*\"([A-Za-z0-9_:.\-]+)\"", T)))
out = {
    "invokeApi_calls": T.count("invokeApi("),
    "endpoints_total_in_deobfuscated": len(found),
    "new_endpoints": new_endpoints,
    "new_states": new_states,
    "new_view_refs": new_views,
    "inline_templates": inline,
    "on_events_in_deobfuscated": socket_types,
}
json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({"invokeApi_calls": out["invokeApi_calls"], "endpoints_seen": len(found), "new_endpoints": len(new_endpoints),
       "new_states": new_states, "new_view_refs": new_views, "inline_templates": len(inline)})
print("new endpoints:", sorted(new_endpoints))

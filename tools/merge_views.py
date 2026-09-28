"""Merge downloaded and embedded views; report include targets that exist in neither.
usage: python tools/merge_views.py <mizito_templates.json> <mizito_embedded_views.json> <out merged.json> <out missing.txt>"""
import json
import sys

remote = json.load(open(sys.argv[1], encoding="utf-8"))
embedded = json.load(open(sys.argv[2], encoding="utf-8"))
merged = {}
for name in sorted(set(remote) | set(embedded)):
    r, e = remote.get(name, {}), embedded.get(name, {})
    if r.get("status") == 200 and e:
        base = dict(e)
        for key in ("texts", "clicks", "models", "srefs", "placeholders", "tooltips", "controllers", "includes"):
            base[key] = sorted(set(r.get(key, [])) | set(e.get(key, [])))
        base["translated"] = {**(r.get("translated") or {}), **(e.get("translated") or {})}
        base["directives"] = r.get("directives", [])
        base["source"] = "views/ + embedded"
    elif e:
        base = dict(e)
        base["source"] = "embedded only (my-include)"
    else:
        base = dict(r)
        base["source"] = "views/ only" if r.get("status") == 200 else f"missing (HTTP {r.get('status')})"
    merged[name] = base
targets = {i for v in merged.values() for i in v.get("includes", [])}
missing = sorted(t for t in targets if t not in merged and not t.startswith(("{", "'")) and "{{" not in t)
json.dump(merged, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(sys.argv[4], "w", encoding="utf-8").write("\n".join(missing))
print({"merged_views": len(merged), "include_targets": len(targets), "missing_targets": len(missing)})
print("missing:", missing)

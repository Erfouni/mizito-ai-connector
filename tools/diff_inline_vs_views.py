"""Is there UI in the bundle's inline HTML that the downloaded views/*.html do not contain?
usage: python tools/diff_inline_vs_views.py <mizito_inline_html.json> <mizito_templates.json>"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
inline = json.load(open(sys.argv[1], encoding="utf-8"))
views = json.load(open(sys.argv[2], encoding="utf-8"))

view_clicks = {c for v in views.values() for c in v.get("clicks", [])}
view_models = {m for v in views.values() for m in v.get("models", [])}
view_texts = {t for v in views.values() for t in v.get("texts", [])} | {t for v in views.values() for t in (v.get("translated") or {}).values() if t}

new = {"clicks": set(), "models": set(), "texts": set()}
where = {}
for owner, o in inline.items():
    if o["library"]:
        continue
    for c in o["clicks"]:
        if c and c not in view_clicks and not c.startswith(("!", "$")):
            new["clicks"].add(c)
            where.setdefault(c, owner)
    for m in o["models"]:
        if m not in view_models:
            new["models"].add(m)
            where.setdefault(m, owner)
    for t in o["texts"]:
        if t not in view_texts and "\"" not in t and "${" not in t and "+" not in t:
            new["texts"].add(t)
print("inline clicks not in views:", len(new["clicks"]))
print(sorted(new["clicks"]))
print("\ninline models not in views:", len(new["models"]))
print(sorted(new["models"])[:120])
print("\ninline texts not in views:", len(new["texts"]))
print(sorted(new["texts"])[:150])
json.dump({k: sorted(v) for k, v in new.items()}, open(sys.argv[1].replace(".json", "_new.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

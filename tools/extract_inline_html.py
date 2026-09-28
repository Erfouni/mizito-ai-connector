"""Every sizeable HTML string in the deobfuscated bundle (not only `template:` properties), with its owner
and the UI it contains. usage: python tools/extract_inline_html.py <deobfuscated.js> <out.json>"""
import html
import json
import re
import sys

T = open(sys.argv[1], encoding="utf-8", errors="replace").read()
LIB = re.compile(r"^(directive|controller|service|factory|provider):\$?(md|Md|mdc|ng|isteven|dynamicLayout)")


def module_before(pos):
    found = list(re.finditer(r"\.(service|factory|controller|directive|filter|component|provider)\(\s*\"([^\"]+)\"", T[max(0, pos - 400000):pos]))
    return f"{found[-1].group(1)}:{found[-1].group(2)}" if found else "(top-level)"


items = []
for m in re.finditer(r"\"((?:[^\"\\\n]|\\.){120,})\"|`([^`]{120,})`", T):
    raw = m.group(1) if m.group(1) is not None else m.group(2)
    body = raw
    if m.group(1) is not None:
        try:
            body = json.loads("\"" + raw + "\"")
        except Exception:
            pass
    if not re.search(r"<(div|span|md-|button|input|a |ul|li|table|form|label|img|i )", body) or "ng-" not in body and "class=" not in body:
        continue
    owner = module_before(m.start())
    texts = sorted({html.unescape(t).strip() for t in re.split(r"<[^>]+>|\{\{.*?\}\}", body)
                    if re.search(r"[؀-ۿ]", t) and len(t.strip()) < 120})
    items.append({
        "owner": owner,
        "library": bool(LIB.match(owner)),
        "pos": m.start(),
        "size": len(body),
        "texts": texts[:60],
        "clicks": sorted({re.split(r"[(\s]", c)[0] for c in re.findall(r"ng-click=\"([^\"]+)\"", body)}),
        "models": sorted(set(re.findall(r"ng-model=\"([^\"]+)\"", body))),
        "srefs": sorted(set(re.findall(r"ui-sref=\"([^\"]+)\"", body))),
    })

by_owner = {}
for it in items:
    o = by_owner.setdefault(it["owner"], {"library": it["library"], "strings": 0, "size": 0, "texts": set(), "clicks": set(), "models": set(), "srefs": set()})
    o["strings"] += 1
    o["size"] += it["size"]
    for k in ("texts", "clicks", "models", "srefs"):
        o[k] |= set(it[k])
out = {k: {**v, **{f: sorted(v[f]) for f in ("texts", "clicks", "models", "srefs")}} for k, v in sorted(by_owner.items())}
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
app = {k: v for k, v in out.items() if not v["library"]}
print({"html_strings": len(items), "owners": len(out), "app_owners": len(app)})
for k, v in app.items():
    print(f"  {k}: {v['strings']} strings, {v['size']} chars | texts {v['texts'][:6]} | clicks {v['clicks'][:8]} | models {v['models'][:6]}")

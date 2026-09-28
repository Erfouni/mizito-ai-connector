"""Templates embedded in the (formerly obfuscated) bundle as {"path.html": "<html>"} and loaded via my-include.
usage: python tools/extract_embedded_views.py <deobfuscated.js> <mizito_map.json> <out.json>"""
import html
import json
import re
import sys

T = open(sys.argv[1], encoding="utf-8", errors="replace").read()
I18N = json.load(open(sys.argv[2], encoding="utf-8"))["i18n"]
INCLUDE = re.compile(r"ng-include=\"'(?:views/)?([^'?]+?)(?:\.html)?(?:\?[^']*)?'\"|templateUrl\('([^']+)'\)|my-include=\"([^\"]+?)(?:\.html)?\"")
TRANSLATE = re.compile(r"'([a-z0-9_]+)'\s*\|\s*translate|translate=\"([a-z0-9_]+)\"")


def analyse(src):
    text_only = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
    visible = re.sub(r"\{\{.*?\}\}", " ", re.sub(r"<[^>]+>", "\n", text_only))
    attrs = lambda a: sorted({html.unescape(v).strip() for v in re.findall(a + r"=\"([^\"]+)\"", src) if v.strip()})
    tkeys = sorted({next(g for g in m.groups() if g) for m in TRANSLATE.finditer(src)})
    return {
        "texts": sorted({html.unescape(t).strip() for t in re.split(r"\n+", visible)
                         if re.search(r"[؀-ۿ]", t) and 1 < len(t.strip()) < 120}),
        "translated": {k: I18N.get(k) for k in tkeys},
        "clicks": sorted({re.split(r"[(\s]", c)[0] for c in attrs("ng-click")}),
        "models": attrs("ng-model"),
        "srefs": attrs("ui-sref"),
        "placeholders": attrs("placeholder"),
        "tooltips": sorted({html.unescape(t).strip() for t in re.findall(r"<md-tooltip[^>]*>(.*?)</md-tooltip>", src, flags=re.S)}),
        "controllers": sorted({c.split(" as ")[0].strip() for c in attrs("ng-controller")}),
        "includes": sorted({next(g for g in m.groups() if g).replace("views/", "").replace(".html", "") for m in INCLUDE.finditer(src)}),
        "size": len(src),
    }


views = {}
for m in re.finditer(r"\"((?:[a-z0-9_\-]+/)+[a-z0-9_\-]+\.html)\"\s*:\s*\"((?:[^\"\\]|\\.)*)\"", T):
    try:
        body = json.loads("\"" + m.group(2) + "\"")
    except Exception:
        continue
    views[m.group(1)[:-5]] = {**analyse(body), "status": 200, "source": "embedded"}
json.dump(views, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({"embedded_views": len(views), "clicks": len({c for v in views.values() for c in v["clicks"]}),
       "models": len({c for v in views.values() for c in v["models"]})})

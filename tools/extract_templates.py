"""Phase 2 of the Mizito site map: download every HTML view (following nested includes) and extract its UI.
Writes /tmp/mizito_templates.json."""
import html
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

MAP = json.load(open("/tmp/mizito_map.json", encoding="utf-8"))
EXTRA = json.load(open("/tmp/mizito_extra.json", encoding="utf-8"))
I18N = MAP["i18n"]
BASE = "https://office.mizito.ir/views/"

queue = set(MAP["templates"]) | set(EXTRA["template_like_strings"]) | {
    "workspace/settings", "workspace/settings_mobile", "workspace/settings_mobile_pages"}
done, results = set(), {}

INCLUDE = re.compile(r"ng-include=\"'(?:views/)?([^'?]+?)(?:\.html)?(?:\?[^']*)?'\"|templateUrl\('([^']+)'\)|src=\"'(?:views/)?([^'?]+?)(?:\.html)?'\"")
TRANSLATE = re.compile(r"'([a-z0-9_]+)'\s*\|\s*translate|translate=\"([a-z0-9_]+)\"|\{\{\s*::?\s*'([a-z0-9_]+)'\s*\|\s*translate")


def fetch(name):
    try:
        req = urllib.request.Request(BASE + name + ".html", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return name, resp.status, resp.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        return name, getattr(exc, "code", 0), ""


def analyse(src):
    text_only = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
    visible = re.sub(r"<[^>]+>", "\n", text_only)
    visible = re.sub(r"\{\{.*?\}\}", " ", visible)
    persian = sorted({html.unescape(t).strip() for t in re.split(r"\n+", visible)
                      if re.search(r"[؀-ۿ]", t) and 1 < len(t.strip()) < 120})
    attrs = lambda a: sorted({html.unescape(v).strip() for v in re.findall(a + r"=\"([^\"]+)\"", src) if v.strip()})
    tkeys = sorted({next(g for g in m.groups() if g) for m in TRANSLATE.finditer(src)})
    return {
        "texts": persian,
        "translated": {k: I18N.get(k) for k in tkeys},
        "clicks": sorted({re.split(r"[(\s]", c)[0] for c in attrs("ng-click")}),
        "click_exprs": attrs("ng-click"),
        "models": attrs("ng-model"),
        "srefs": attrs("ui-sref"),
        "placeholders": attrs("placeholder"),
        "aria_labels": attrs("aria-label"),
        "tooltips": sorted({html.unescape(t).strip() for t in re.findall(r"<md-tooltip[^>]*>(.*?)</md-tooltip>", src, flags=re.S)}),
        "tab_labels": attrs("label") + attrs("md-tab-label"),
        "inputs": sorted(set(re.findall(r"<input[^>]*type=\"([a-z]+)\"", src))),
        "controllers": sorted({c.split(" as ")[0].strip() for c in attrs("ng-controller")}),
        "directives": sorted(set(re.findall(r"<([a-z]+(?:-[a-z]+)+)[\s>/]", src)) - {"md-button", "md-icon", "md-menu", "md-menu-item", "md-menu-content", "md-tooltip", "md-input-container", "md-checkbox", "md-switch", "md-select", "md-option", "md-dialog", "md-dialog-content", "md-dialog-actions", "md-toolbar", "md-content", "md-list", "md-list-item", "md-tabs", "md-tab", "md-progress-circular", "md-progress-linear", "md-radio-group", "md-radio-button", "md-chips", "md-autocomplete", "md-datepicker", "md-divider", "md-subheader", "md-card", "md-card-content", "md-sidenav", "md-slider", "md-grid-list", "md-grid-tile", "md-virtual-repeat-container", "md-chip-template", "md-item-template", "md-not-found", "md-tab-label", "md-tab-body", "md-card-actions", "md-card-title", "md-fab-speed-dial", "md-fab-trigger", "md-fab-actions", "md-whiteframe", "md-optgroup", "md-contact-chips", "md-bottom-sheet", "md-panel"}),
        "size": len(src),
    }


with ThreadPoolExecutor(max_workers=8) as pool:
    while queue - done:
        batch = sorted(queue - done)
        done |= set(batch)
        for name, status, src in pool.map(fetch, batch):
            if status != 200 or not src:
                results[name] = {"status": status}
                continue
            info = analyse(src)
            includes = set()
            for m in INCLUDE.finditer(src):
                inc = next(g for g in m.groups() if g)
                includes.add(inc.replace("views/", "").replace(".html", ""))
            info["includes"] = sorted(includes)
            info["status"] = 200
            results[name] = info
            queue |= includes

json.dump(results, open("/tmp/mizito_templates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok = sum(1 for r in results.values() if r.get("status") == 200)
print({"templates_total": len(results), "downloaded": ok, "failed": len(results) - ok,
       "failed_names": sorted(k for k, r in results.items() if r.get("status") != 200)[:40]})

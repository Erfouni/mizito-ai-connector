"""Build docs/site-map/ from the raw extraction files of the Mizito web client.

Inputs (from tools/extract_*.py, run on a host that can reach office.mizito.ir):
  mizito_map.json, mizito_extra.json, mizito_events.json, mizito_templates.json
usage: python tools/build_site_map.py <dir with the json files>
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1])
OUT = ROOT / "docs" / "site-map"
OUT.mkdir(parents=True, exist_ok=True)

MAP = json.loads((SRC / "mizito_map.json").read_text(encoding="utf-8"))
EXTRA = json.loads((SRC / "mizito_extra.json").read_text(encoding="utf-8"))
EVENTS = json.loads((SRC / "mizito_events.json").read_text(encoding="utf-8"))
MERGED = SRC / "mizito_views_merged.json"  # views/*.html + templates embedded in the bundle (my-include)
VIEWS = json.loads((MERGED if MERGED.exists() else SRC / "mizito_templates.json").read_text(encoding="utf-8"))
JS_STRINGS = json.loads((SRC / "mizito_js_strings.json").read_text(encoding="utf-8")) if (SRC / "mizito_js_strings.json").exists() else []
PARENTS = defaultdict(set)
for _name, _v in VIEWS.items():
    for _inc in _v.get("includes", []):
        PARENTS[_inc].add(_name)
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")

# ---------------------------------------------------------------------------------------------
# MCP coverage: which server.py function calls which endpoint, plus what the tests established.
# ---------------------------------------------------------------------------------------------
defs = [(m.start(), m.group(1)) for m in re.finditer(r"^\s*def (\w+)\(", SERVER, flags=re.M)]
mcp_use: dict[str, set[str]] = defaultdict(set)
for m in re.finditer(r"client\.(?:call|_post)\(\s*\"([\w.]+)\"", SERVER):
    owner = [name for pos, name in defs if pos < m.start()]
    mcp_use[m.group(1)].add(owner[-1] if owner else "?")
# endpoints called with a computed name inside server.py
for name in ("chat.pinDialog", "chat.unpinDialog"):
    mcp_use[name].add("mizito_manage_conversation")

TESTED = {
    "workspace.userId", "workspace.getUsers", "workspace.planInfo", "dashboard.getAllSummary",
    "chat.getDialogs", "chat.getFullChat", "chat.getChatView", "chat.getHistory", "chat.search", "chat.send",
    "chat.seen", "chat.getMessages", "chat.createDialog", "chat.updateTitle", "chat.pinDialog", "chat.unpinDialog",
    "chat.addPinMessage", "chat.toggleBookmark", "chat.archiveProject",
    "projects.getList", "projects.allSummary", "projects.full", "projects.add", "projects.save",
    "projects.addKanbanBoard", "projects.history",
    "tasks.upcoming", "tasks.getAll", "tasks.get", "tasks.add", "tasks.save", "tasks.newComment", "tasks.getComments",
    "tasks.setCompleted", "tasks.updateDeadline", "tasks.updateProgress", "tasks.setChecklistCheckedValue",
    "tasks.snooze", "tasks.toggleBookmark", "tasks.history", "tasks.badge",
    "inbox.getInbox", "inbox.getHistory", "inbox.send", "inbox.archive", "inbox.unArchive", "inbox.toggleBookmark",
    "inbox.seen",
    "notes.getAll", "notes.create", "notes.update", "notes.archiveNote", "notes.updatePinState", "notes.setChecklistValue",
    "labels.getAll", "labels.add",
}
UNTESTED_NOTES = {
    "tasks.removeTask": "حذف است؛ تست نشد",
    "tasks.removeTaskUndo": "برگرداندن حذف؛ تست نشد",
    "chat.removeSentMessage": "حذف است؛ تست نشد",
    "chat.inviteUser": "به همکار واقعی اعلان می‌رود؛ تست نشد",
    "chat.updateSentMessage": "فقط برای پیام دیده‌نشده؛ مسیر موفق تست نشد",
    "notes.deleteNote": "حذف است؛ تست نشد",
    "inbox.changeMessageLabels": "تست نشد",
    "workspace.inviteMember": "دعوت واقعی می‌فرستد؛ تست نشد",
    "workspace.switch": "حساب تست فقط یک میزکار داشت",
    "customer.add": "پشت MIZITO_ENABLE_CRM؛ روی حساب تست 400 داد",
}
REFUSED = {
    "projects.archive": "405 برای غیرمدیر (در وب «حذف با امکان بازگشت» است)",
    "projects.undoArchive": "405 برای غیرمدیر",
    "customer.add": "400 حتی با payload دقیق فرم وب (CRM در پلن نیست)",
    "deal.getAll": "400 (فروش در پلن نیست)",
    "deal.getReportStatistics": "400 (فروش در پلن نیست)",
    "monitor.workspace": "400 (دسترسی مدیر/پلن)",
    "monitor.project": "400 (دسترسی مدیر/پلن)",
    "projects.monitor.project": "400 (دسترسی مدیر/پلن)",
}
MODULE_FA = {
    "attendance": "حضور و غیاب", "chat": "گفتگو", "content": "فایل و محتوا", "customer": "CRM – مشتریان",
    "dashboard": "داشبورد", "deal": "CRM – معاملات", "device": "دستگاه و اعلان", "feedback": "بازخورد",
    "fix": "ابزار اصلاح داده (مدیر)", "formRequestTemplate": "فرم‌های درخواست", "inbox": "کارتابل نامه‌ها",
    "labels": "برچسب‌ها", "meeting": "جلسه‌ی تصویری", "minute": "صورتجلسه", "minuteAdvanced": "صورتجلسه‌ی پیشرفته",
    "monitor": "گزارش و مانیتورینگ", "notes": "یادداشت‌ها", "payment": "پرداخت و صورتحساب", "polling": "نظرسنجی",
    "profile": "پروفایل و امنیت حساب", "projectAutomation": "اتوماسیون پروژه",
    "projectAutomationWorkflow": "گردش‌کار اتوماسیون", "projects": "پروژه‌ها", "session": "نشست و حساب کاربری",
    "support": "پشتیبانی میزیتو", "taskTemplates": "قالب‌های وظیفه", "tasks": "وظایف", "workspace": "میزکار",
}
EXCLUDED_WHY = {
    "payment": "مالی و پرداخت: عمداً کنار گذاشته شد",
    "session": "ورود، ثبت‌نام و حذف حساب: عمداً کنار گذاشته شد",
    "profile": "رمز، شماره، نشست‌ها و امنیت حساب: عمداً کنار گذاشته شد",
    "support": "گفتگوی پشتیبانی خود میزیتو: خارج از محدوده",
    "fix": "ابزار اصلاح دسترسی مدیر: خارج از محدوده",
    "attendance": "حضور و غیاب: پیاده نشد",
    "meeting": "تماس تصویری (WebRTC): از طریق MCP قابل استفاده نیست",
    "projectAutomation": "اتوماسیون پروژه‌های پیشرفته: پیاده نشد",
    "projectAutomationWorkflow": "گردش‌کار اتوماسیون: پیاده نشد",
    "formRequestTemplate": "فرم‌های درخواست (پلن سازمانی): پیاده نشد",
    "minute": "صورتجلسه (به‌صورت پیوست چت ساخته می‌شود): پیاده نشد",
    "minuteAdvanced": "صورتجلسه‌ی پیشرفته: پیاده نشد",
    "polling": "نظرسنجی (پیوست چت، نیازمند ادمین گروه): پیاده نشد",
    "customer": "CRM: پلن حساب تست شامل آن نبود",
    "deal": "CRM فروش: پلن حساب تست شامل آن نبود",
    "monitor": "گزارش‌ها: دسترسی مدیر یا پلن لازم",
    "taskTemplates": "قالب وظیفه: پیاده نشد",
    "device": "ثبت دستگاه برای اعلان: خارج از محدوده",
    "feedback": "بازخورد به میزیتو: خارج از محدوده",
    "content": "برش عکس: خارج از محدوده",
}
READ_METHOD = re.compile(r"^(get\w*|search\w*|history|info|upcoming|badge|allSummary|chatSummary|full|userInfo|userId|name|planInfo|expandInboxRow)$")
BLOCKED = {"session", "profile", "payment", "support", "fix"}


def coverage(ep: str) -> tuple[str, str]:
    module, _, method = ep.rpartition(".")
    root = module.split(".")[0]
    tools = sorted(mcp_use.get(ep, set()))
    via = ", ".join(f"`{t}`" for t in tools)
    if ep in REFUSED:
        return "⛔ رد شد", REFUSED[ep] + (f" — {via}" if via else "")
    if ep in TESTED:
        return "✅ تست‌شده", via or "`mizito_api_read`"
    if tools:
        return "🟡 پیاده‌شده، تست‌نشده", via + (f" — {UNTESTED_NOTES[ep]}" if ep in UNTESTED_NOTES else "")
    if root not in BLOCKED and (root == "monitor" or READ_METHOD.match(method)):
        return "🔎 با `mizito_api_read`", "خواندنی؛ ابزار اختصاصی ندارد"
    return "➖ پیاده‌نشده", EXCLUDED_WHY.get(root, "پیاده نشد")


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def code(x) -> str:
    return f"`{x}`" if x else "—"


def esc(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def clean_text(t: str) -> str:
    """Drop markup and attribute leftovers that the regex-based HTML split leaves in visible text."""
    t = re.sub(r"<[^>]*>", " ", str(t))
    if '">' in t:
        t = t.split('">')[-1]
    return re.sub(r"\s+", " ", t).strip(" ,،")


def short_list(items, n=40, sep="، "):
    items = [esc(i) for i in dict.fromkeys(clean_text(x) if not str(x).startswith("`") else x for x in items if x) if i]
    more = f"{sep}… (+{len(items) - n})" if len(items) > n else ""
    return sep.join(items[:n]) + more if items else "—"


def view_controllers(name: str, seen=None) -> set[str]:
    seen = seen or set()
    if name in seen or name not in VIEWS:
        return set()
    seen.add(name)
    v = VIEWS[name]
    found = set(v.get("controllers", []))
    for inc in v.get("includes", []):
        found |= view_controllers(inc, seen)
    return found


endpoints_by_module_site: dict[str, set[str]] = defaultdict(set)
for ep, info in MAP["endpoints"].items():
    for site in info["sites"]:
        endpoints_by_module_site[site["module"]].add(ep)

# ---------------------------------------------------------------------------------------------
# pages.md
# ---------------------------------------------------------------------------------------------
AREAS = [
    ("پوسته‌ی اپ", lambda n: n == "ws"),
    ("ورود، ثبت‌نام و حساب کاربری", lambda n: n.split(".")[0] in {"login", "login_sso", "register", "delete_account", "workspace_switching"}),
    ("داشبورد", lambda n: n == "ws.home"),
    ("گفتگو", lambda n: n == "ws.im"),
    ("پروژه‌ها", lambda n: n.startswith(("ws.projects", "ws.import_project"))),
    ("وظایف و تقویم", lambda n: n.startswith("ws.tasks")),
    ("کارتابل نامه‌ها", lambda n: n.startswith("ws.inbox")),
    ("یادداشت‌ها", lambda n: n.startswith("ws.notes")),
    ("CRM: مشتریان، معاملات، پرداخت‌ها", lambda n: n.startswith(("ws.customer", "ws.import_customers"))),
    ("مانیتورینگ و گزارش‌ها", lambda n: n.startswith("ws.monitoring")),
    ("جستجو و نشان‌شده‌ها", lambda n: n in {"ws.search", "ws.bookmarks"}),
    ("تنظیمات میزکار", lambda n: n.startswith("ws.settings")),
    ("جلسه‌ی تصویری", lambda n: n == "ws.meeting"),
    ("پشتیبانی", lambda n: n == "ws.support"),
    ("چاپ", lambda n: n == "ws.print"),
    ("ابزارهای اصلاح داده (مدیر)", lambda n: n.startswith("ws.fix")),
]
states = list(MAP["states"]) + [
    {"name": "delete_account.request", "url": "(کنترلر AppDeleteAccountRequest…)", "template": None, "controller": None,
     "abstract": False, "params": [], "redirect": None},
    {"name": "delete_account.validation", "url": "(کنترلر AppDeleteAccountController)", "template": None, "controller": None,
     "abstract": False, "params": [], "redirect": None},
]
SETTINGS_TABS = {
    "invite": "دعوت عضو جدید", "members": "اعضا", "perms": "مجوزها", "plan": "طرح فعلی", "plans": "خرید/ارتقای طرح",
    "removed": "اعضای حذف‌شده",
}

lines = [
    "# صفحه‌های میزیتو (office.mizito.ir)",
    "",
    "هر صفحه (state) با آدرس، قالب HTML، پارامترها، و چیزهایی که در قالبش هست: متن‌ها، دکمه‌ها و عمل‌ها (`ng-click`)،",
    "فیلدها (`ng-model`)، لینک‌ها (`ui-sref`)، کنترلرها و endpointهایی که آن کنترلرها صدا می‌زنند.",
    "جزئیات هر قالب در [views.md](views.md) و هر endpoint در [api.md](api.md) آمده است.",
    "",
]
placed = set()
for area, pred in AREAS:
    group = [s for s in states if pred(s["name"])]
    if not group:
        continue
    lines += [f"## {area}", ""]
    for s in group:
        placed.add(s["name"])
        lines.append(f"### `{s['name']}`" + (" (انتزاعی)" if s.get("abstract") else ""))
        lines.append("")
        lines.append(f"- آدرس: `#{s['url']}`" if s.get("url") and not s["url"].startswith("(") else f"- آدرس: {s.get('url') or '—'}")
        lines.append(f"- قالب: {code(s.get('template'))}")
        if s.get("params"):
            lines.append(f"- پارامترها: {', '.join(f'`{p}`' for p in s['params'] if p not in ('value', 'dynamic'))}")
        if s.get("redirect"):
            lines.append(f"- انتقال به: `{s['redirect']}`")
        v = VIEWS.get(s.get("template") or "", {})
        if v:
            texts = v.get("texts", []) + [t for t in (v.get("translated") or {}).values() if t]
            lines.append(f"- متن‌ها: {short_list(sorted(set(texts)), 30)}")
            lines.append(f"- عمل‌ها: {short_list(['`' + c + '`' for c in v.get('clicks', [])], 60, ' ')}")
            if v.get("models"):
                lines.append(f"- فیلدها: {short_list(['`' + m + '`' for m in v['models']], 40, ' ')}")
            if v.get("srefs"):
                lines.append(f"- لینک‌ها: {short_list(['`' + x + '`' for x in v['srefs']], 30, ' ')}")
            if v.get("includes"):
                lines.append(f"- زیرقالب‌ها: {short_list(['`' + x + '`' for x in v['includes']], 30, ' ')}")
        ctrls = sorted(view_controllers(s.get("template") or ""))
        if ctrls:
            lines.append(f"- کنترلرها: {' '.join('`' + c + '`' for c in ctrls)}")
            eps = sorted({e for c in ctrls for e in endpoints_by_module_site.get(f"controller:{c}", set())})
            if eps:
                lines.append(f"- endpointهای این کنترلرها: {' '.join('`' + e + '`' for e in eps)}")
        if s["name"] == "ws.settings":
            lines.append("- زیرصفحه‌ها (`:page`): " + "، ".join(f"`{k}` ({v})" for k, v in SETTINGS_TABS.items())
                         + "؛ به‌علاوه‌ی تب «عمومی» و «مالی» در خود قالب")
        lines.append("")
missing_states = [s["name"] for s in states if s["name"] not in placed]
assert not missing_states, missing_states
(OUT / "pages.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------------------------
# views.md
# ---------------------------------------------------------------------------------------------
state_by_tpl = defaultdict(list)
for s in states:
    if s.get("template"):
        state_by_tpl[s["template"]].append(s["name"])
lines = [
    "# قالب‌ها، مودال‌ها و پنل‌های میزیتو",
    "",
    f"همه‌ی {len(VIEWS)} قالب HTML: آن‌هایی که از `https://office.mizito.ir/views/<نام>.html` بار می‌شوند، به‌علاوه‌ی قالب‌هایی",
    "که داخل کد مبهم‌شده‌ی `a_.js` جاسازی شده‌اند و با `my-include` بار می‌شوند (منوی کناری، هدر، ورودی چت، کانبان، گانت، ...).",
    "برای هر قالب: کجا استفاده می‌شود (صفحه، یا سرویس/کنترلر و تابعی که مودال را باز می‌کند)، متن‌ها، عمل‌ها، فیلدها،",
    "کنترلرها و عناصر سفارشی.",
    "",
]
folders = defaultdict(list)
for name in sorted(VIEWS):
    folders[name.split("/")[0] if "/" in name else "(ریشه)"].append(name)
for folder in sorted(folders):
    lines += [f"## `{folder}/` ({len(folders[folder])})", ""]
    for name in folders[folder]:
        v = VIEWS[name]
        lines.append(f"### `{name}`")
        lines.append("")
        if v.get("status") != 200:
            lines.append(f"- دانلود نشد (HTTP {v.get('status')}); این قالب پویا ساخته می‌شود.")
            lines.append("")
            continue
        uses = state_by_tpl.get(name, [])
        ctx = (MAP["templates"].get(name) or {}).get("contexts", [])
        where = ([f"صفحه‌ی `{u}`" for u in uses] + [f"`{c}`" for c in ctx]
                 + [f"داخل قالب `{p}`" for p in sorted(PARENTS.get(name, []))])
        lines.append(f"- منبع: {v.get('source', 'views/')}")
        lines.append(f"- استفاده: {short_list(where, 12, '؛ ')}")
        texts = v.get("texts", []) + [t for t in (v.get("translated") or {}).values() if t]
        lines.append(f"- متن‌ها: {short_list(sorted(set(texts)), 25)}")
        if v.get("clicks"):
            lines.append(f"- عمل‌ها: {short_list(['`' + c + '`' for c in v['clicks']], 50, ' ')}")
        if v.get("models"):
            lines.append(f"- فیلدها: {short_list(['`' + m + '`' for m in v['models']], 30, ' ')}")
        extra = v.get("placeholders", []) + v.get("tooltips", [])
        if extra:
            lines.append(f"- راهنماها: {short_list(extra, 15)}")
        if v.get("controllers"):
            lines.append(f"- کنترلر: {' '.join('`' + c + '`' for c in v['controllers'])}")
        if v.get("directives"):
            lines.append(f"- عناصر سفارشی: {' '.join('`' + d + '`' for d in v['directives'])}")
        if v.get("includes"):
            lines.append(f"- زیرقالب: {' '.join('`' + i + '`' for i in v['includes'])}")
        lines.append("")
(OUT / "views.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------------------------
# api.md
# ---------------------------------------------------------------------------------------------
by_module = defaultdict(list)
for ep in sorted(MAP["endpoints"]):
    by_module[ep.split(".")[0]].append(ep)
status_count = defaultdict(int)
rows_all = {}
for ep in MAP["endpoints"]:
    status, note = coverage(ep)
    status_count[status] += 1
    rows_all[ep] = (status, note)
lines = [
    "# همه‌ی endpointهای API میزیتو",
    "",
    f"{len(MAP['endpoints'])} endpoint از کد وب‌اپ، از جمله آن‌هایی که اسمشان با عبارت شرطی ساخته می‌شود. همه `POST {{api_url}}/api/<ماژول>/<متد>` با هدر `x-token` هستند.",
    "«پارامترها» کلیدهای payload در محل فراخوانی‌اند (`var:x` یعنی شیء از قبل ساخته شده، `-` یعنی بدون payload).",
    "«محل فراخوانی» سرویس یا کنترلر و تابعی در کد وب است که آن را صدا می‌زند.",
    "",
    "| وضعیت در MCP | تعداد |",
    "|---|---|",
] + [f"| {k} | {v} |" for k, v in sorted(status_count.items())] + [""]
for module in sorted(by_module):
    eps = by_module[module]
    lines += [f"## `{module}` — {MODULE_FA.get(module, module)} ({len(eps)})", "",
              "| endpoint | پارامترها | محل فراخوانی در وب | MCP | توضیح |", "|---|---|---|---|---|"]
    for ep in eps:
        info = MAP["endpoints"][ep]
        params = " \\| ".join(f"`{p}`" for p in info["params"])
        sites = "<br>".join(sorted({f"{s['module']} › {s['function'] or '?'}" for s in info["sites"]})[:6])
        status, note = rows_all[ep]
        lines.append(f"| `{ep}` | {params} | {esc(sites)} | {status} | {esc(note)} |")
    lines.append("")
lines += [
    "## درخواست‌های دیگر (غیر از `invokeApi`)",
    "",
    "| مسیر | کاربرد |",
    "|---|---|",
    "| `POST {api_url}/capi/session/create` | ورود: `{username, password: md5\\|sha256, loginCode, regId}` → `{status, token}` |",
    "| `POST {api_url}/capi/<module>/<method>` | فراخوانی بدون توکن (گزینه‌ی `no_token` در `invokeApi`) |",
    "| `POST {api_url}/api/content/upload` | آپلود فایل و عکس (مسیر از `getUploadPath`) |",
    "| `POST {api_url}/api/crm/report` | گزارش چاپی CRM با فرم HTML (برچسب‌ها و فیلترها) |",
    "| `GET {cdn_url}/cdn/<jwt>` | نمایش فایل و عکس (JWT شامل شناسه‌ی محتوا و میزکار) |",
    "| `GET {cdn_url}/cdn/dl/…` | دانلود فایل |",
    "| `GET {cdn_url}/cdn/de/logo/…` | لوگوی سرور اختصاصی |",
    "| `socket.io {io_url}` | کانال لحظه‌ای؛ جزئیات در [realtime-and-types.md](realtime-and-types.md) |",
    "",
]
(OUT / "api.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------------------------
# realtime-and-types.md
# ---------------------------------------------------------------------------------------------
access_real = sorted(a for a in MAP["access_flags"] if re.fullmatch(r"access_(admin|advanced|chat_advanced|chat_group_creator|crm|crm_creator|crm_print|guest_contacts|is_guest|monitoring|owner|project_creator|project_monitoring|sales|sales_monitoring|sales_payments|sales_payments_monitoring|secretariat|settings|support_admin|support_attendance|support_feedback_monitor|time\w*|workspace_role_names)", a))
lines = [
    "# لحظه‌ای، انواع داده، پلن‌ها و تنظیمات میزیتو",
    "",
    "## کانال لحظه‌ای (socket.io)",
    "",
    "- اتصال: `io(Config.App.io_url, {query: \"tab_id=<id>\", transports: [\"websocket\"], path: \"/\" + io_url_path})`.",
    "- بعد از `connect`، کلاینت `emit(\"authenticate\", {token})` می‌فرستد. خطای `Unauthorized` یعنی توکن نامعتبر است.",
    "- همه‌ی به‌روزرسانی‌ها با رویداد `m` می‌آیند: `{type, body, workspace_id}`. کلاینت `type` را در میزکار فعلی پخش می‌کند و برای میزکارهای دیگر با پیشوند `out_workspace_`.",
    "- رویدادهای کنترلی: `connect_error`، `disconnect`، `terminated`، `reconnect_socket`. نوع‌های خاص روی `m`: `invite_to_workspace` و `dashboard_seen`.",
    "",
    f"### نوع‌های پیام سرور که برای میزکارهای دیگر هم گوش داده می‌شوند ({len(EVENTS['out_workspace_events'])})",
    "",
    " ".join(f"`{e}`" for e in EVENTS["out_workspace_events"]),
    "",
    f"### همه‌ی رویدادهایی که کلاینت گوش می‌دهد ولی خودش پخش نمی‌کند ({len(EVENTS['server_pushed_candidates'])})",
    "",
    "این‌ها یا از سرور می‌آیند یا از کتابخانه‌های رابط (drag، gantt، تقویم):",
    "",
    " ".join(f"`{e}`" for e in EVENTS["server_pushed_candidates"]),
    "",
    f"## انواع محتوای پیام چت ({len(EXTRA['media_types'])})",
    "",
    " ".join(f"`{e}`" for e in EXTRA["media_types"]),
    "",
    f"## رویدادهای سیستمی داخل گفتگو ({len(EXTRA['action_types'])})",
    "",
    " ".join(f"`{e}`" for e in EXTRA["action_types"]),
    "",
    "## قالب‌بندی متن پیام",
    "",
    " ".join(f"`{e}`" for e in EXTRA["case_labels"] if e.startswith("messageEntity")),
    "",
    f"## محدودیت‌های پلن (`checkPlanOption`) ({len(MAP['plan_options'])})",
    "",
    " ".join(f"`{e}`" for e in MAP["plan_options"]),
    "",
    f"## پرچم‌های دسترسی کاربر ({len(access_real)})",
    "",
    " ".join(f"`{e}`" for e in access_real),
    "",
    f"## تنظیمات سراسری اپ (`Config.App`) ({len(MAP['config_keys'])})",
    "",
    " ".join(f"`{e}`" for e in MAP["config_keys"] if e != "lastPanelRef"),
    "",
    f"## کلیدهای localStorage ({len(MAP['local_storage'])})",
    "",
    " ".join(f"`{e}`" for e in MAP["local_storage"]),
    "",
    f"## همه‌ی مقصدهای ناوبری در کد (`$state.go`) ({len(EXTRA['state_go_targets'])})",
    "",
    " ".join(f"`{e}`" for e in EXTRA["state_go_targets"]),
    "",
    f"## ماژول‌های AngularJS ({len(MAP['modules'])})",
    "",
]
kinds = defaultdict(list)
for mod in MAP["modules"]:
    kinds[mod["kind"]].append(mod["name"])
for kind in sorted(kinds):
    lines += [f"- **{kind}** ({len(kinds[kind])}): " + " ".join(f"`{n}`" for n in kinds[kind])]
lines += ["", f"## دیکشنری ترجمه ({len(MAP['i18n'])} کلید)", "", "کامل در `site_map.json` زیر کلید `i18n`.", ""]
(OUT / "realtime-and-types.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------------------------
# README.md + site_map.json
# ---------------------------------------------------------------------------------------------
tools = sorted(set(re.findall(r"def (mizito_\w+)\(", SERVER)))
counts = [
    ("صفحه‌ها (state)", len(states)), ("قالب‌های HTML", len(VIEWS)), ("endpointهای API", len(MAP["endpoints"])),
    ("ماژول‌های API", len(by_module)), ("ماژول‌های AngularJS", len(MAP["modules"])),
    ("کنترلرهای ارجاع‌شده در قالب‌ها", len({c for v in VIEWS.values() for c in v.get("controllers", [])})),
    ("عناصر سفارشی رابط", len({d for v in VIEWS.values() for d in v.get("directives", [])})),
    ("نوع‌های پیام سرور (out_workspace)", len(EVENTS["out_workspace_events"])),
    ("انواع محتوای پیام", len(EXTRA["media_types"])), ("رویدادهای سیستمی گفتگو", len(EXTRA["action_types"])),
    ("محدودیت‌های پلن", len(MAP["plan_options"])), ("پرچم‌های دسترسی", len(access_real)),
    ("تنظیمات Config.App", len(MAP["config_keys"]) - 1), ("کلیدهای localStorage", len(MAP["local_storage"])),
    ("کلیدهای ترجمه", len(MAP["i18n"])), ("رشته‌های فارسی داخل کد", len(JS_STRINGS)),
    ("قالب‌های فقط جاسازی‌شده", sum(1 for v in VIEWS.values() if "embedded only" in v.get("source", ""))),
    ("ابزارهای MCP این ریپو", len(tools)),
]
readme = [
    "# نقشه‌ی کامل میزیتو",
    "",
    f"نقشه‌ی وب‌اپ `office.mizito.ir`، ساخته‌شده در {date.today().isoformat()} از کد خود وب‌اپ (`a_.js`، حدود ۱۰ مگابایت)",
    f"و همه‌ی قالب‌های HTML آن. نسخه‌ی کد: `cache_id` در `Config.App`. اگر میزیتو به‌روز شد، با `tools/` دوباره بسازید.",
    "",
    "| فایل | محتوا |",
    "|---|---|",
    "| [pages.md](pages.md) | صفحه به صفحه، گروه‌بندی‌شده بر اساس بخش‌های سایت |",
    "| [views.md](views.md) | همه‌ی قالب‌ها، مودال‌ها و پنل‌ها |",
    "| [api.md](api.md) | همه‌ی endpointها با پارامترها، محل فراخوانی و وضعیت در MCP |",
    "| [realtime-and-types.md](realtime-and-types.md) | socket.io، انواع پیام، پلن‌ها، دسترسی‌ها و تنظیمات |",
    "| [site_map.json](site_map.json) | همه‌ی داده‌های خام، ماشین‌خوان |",
    "",
    "## آمار",
    "",
    "| مورد | تعداد |",
    "|---|---|",
] + [f"| {k} | {v} |" for k, v in counts] + [
    "",
    "## روش ساخت و اطمینان از کامل بودن",
    "",
    "1. **استخراج ایستا:** از `a_.js` این‌ها درآمد: صفحه‌ها، قالب‌ها، ماژول‌ها، `invokeApi`ها، فراخوانی‌های غیرمستقیم (`y(…)`، `w(…)` و انتخاب شرطی)، درخواست‌های مستقیم، socket، پلن‌ها، دسترسی‌ها و ترجمه‌ها.",
    "2. **رمزگشایی:** حدود نیمی از `a_.js` مبهم‌سازی شده است و با [webcrack](https://github.com/j4k0xb/webcrack) رمزگشایی شد.",
    "   در این بخش endpoint یا صفحه‌ی پنهانی نبود، ولی ۳۱۸ قالب جاسازی‌شده داشت که ۱۱۷ تای آن در `views/` نیستند.",
    "3. **دانلود و تحلیل قالب‌ها:** همه‌ی قالب‌ها دانلود و تحلیل شدند و `ng-include`، `my-include` و `templateUrl` تا انتها دنبال شدند. هیچ ارجاع حل‌نشده‌ای نماند.",
    "4. **بررسی متقاطع:** همه‌ی عمل‌ها (`ng-click`) و فیلدهای (`ng-model`) موجود در HTMLهای کد در این نقشه هستند.",
    "   هر صفحه، قالب و endpoint در سندها آمده است و `tools/check_site_map.py` این را خودکار چک می‌کند.",
    "",
    "## معماری در یک نگاه",
    "",
    "- **رابط:** AngularJS همراه با ui-router و Angular Material، با آدرس‌های `#/…`. پیش‌فرض راست‌به‌چپ و تقویم شمسی است.",
    "- **API:** همه `POST {api_url}/api/<module>/<method>` هستند، با هدر `x-token` و بدنه‌ی JSON. خطای 401 یعنی نشست منقضی شده.",
    "  درخواست‌های بدون توکن از `/capi/…` می‌روند (ورود: `/capi/session/create`).",
    "- **فایل:** آپلود به `/api/content/upload` است و نمایش و دانلود از CDN با آدرس‌های JWT.",
    "- **لحظه‌ای:** socket.io روی `io_url` است و همه‌ی رویدادها با کانال `m` می‌آیند.",
    "- **میزکار:** هر توکن به یک میزکار بسته است و `workspace.switch` توکن تازه می‌دهد.",
    "",
    "## بخش‌های سایت",
    "",
    "### منوی کناری و هدر",
    "",
    "- **منوی کناری** (`partial/side-nav-menu`) ۹ بخش دارد: داشبورد، گفتگو، پروژه‌ها، وظایف، نامه‌ها، یادداشت‌ها، مشتریان، مانیتورینگ و پشتیبانی.",
    "  همچنین فهرست همکاران (وضعیت آنلاین، شروع گفتگو، تبریک تولد)، دعوت عضو جدید، و فهرست میزکارها (ساخت، تعویض، تنظیمات) را دارد.",
    "- **هدر** (`partial/header`): جستجو، نشان‌شده‌ها، تاریخچه‌ی اعلان‌ها، حالت روز یا شب یا سیستم، پس‌زمینه، توقف اعلان‌ها،",
    "  قابلیت‌های جدید، راهنما و راهنمای نسخه‌ی دمو، ارسال پیشنهاد، ارتباط با پشتیبانی، تمدید یا ارتقای طرح،",
    "  تنظیمات میزکار و پروفایل، دانلود اپ iOS و اندروید، و خروج.",
    "",
    "### بخش‌ها",
    "",
    "- **ورود و حساب:** ورود (همراه ورود دومرحله‌ای)، SSO، فراموشی و بازیابی رمز، ثبت‌نام ۴ مرحله‌ای، تکمیل پروفایل،",
    "  حذف حساب (درخواست و تأیید با کد)، تعویض میزکار.",
    "- **پروفایل:** تب اطلاعات (نام، تاریخ تولد، عکس)، تب ایمیل (تأیید و اعلان ایمیلی)، و تب امنیت (ورود دومرحله‌ای، رمز، نشست‌ها، سابقه‌ی ورود).",
    "- **داشبورد:** سلام و وضعیت، ویجت‌ها (کارهای من، پیگیری‌ها، پروژه‌های من، بیشترین تأخیر، گزارش‌ها)، همکاران،",
    "  سایر میزکارها، دعوت‌ها، جلسه‌های در انتظار، و ارتقای طرح.",
    "- **گفتگو:** گفتگوی خصوصی، گروه، کانال، گفتگوی پروژه و گفتگوی مشتری، به‌همراه فهرست گفتگوها، فیلتر، سنجاق و هدر گفتگو.",
    "  - محتوای پیام: متن قالب‌بندی‌شده، عکس، فایل، صدا (ضبط)، ویدئو، استیکر، وظیفه، صورتجلسه، نظرسنجی و گزارش تماس.",
    "  - کارهای روی پیام: پاسخ، ارجاع، ویرایش و حذف، پیش‌نویس، دستورهای ربات، و جلسه‌ی آنلاین.",
    "- **پروژه‌ها:**",
    "  - نماها: فهرست پروژه‌ها (گفتگوهای پروژه)، کانبان با ستون‌ها، گانت (فازها، وابستگی‌ها، چاپ)، و تقویم پروژه‌ها.",
    "  - تنظیمات: امکانات پیشرفته (وزن، مهلت، گانت، صورتجلسه‌ی پیشرفته، اتوماسیون)، اعضا و ادمین‌ها و دسترسی گانت.",
    "  - اتوماسیون: قانون، شرط، اقدام، دکمه، فرم، پارامتر سفارشی، گردش‌کار و گزارش.",
    "  - کارهای دیگر: فرم‌های درخواست، قالب وظیفه، کپی پروژه، ورود پروژه از فایل، و بایگانی.",
    "- **وظایف:** کارهای من، پیگیری از دیگران، انجام‌شده، تقویم (بر اساس یادآوری یا مهلت)، برچسب‌ها و دسته‌بندی.",
    "  - جزئیات هر وظیفه: یادآوری و تکرار، مهلت و شروع، چک‌لیست، کامنت با پیوست، مسئول تأیید نهایی، رونوشت، پیشرفت،",
    "    وزن، پارامترهای سفارشی، لینک اشتراک و تاریخچه.",
    "- **کارتابل:** ورودی، خروجی، پاراف‌ها، بایگانی و برچسب‌ها.",
    "  - کارهای روی نامه: پاسخ، ارجاع، چاپ، اتصال به پرونده‌ی مشتری، و ثبت در دبیرخانه (وارده و صادره با شماره و تاریخ).",
    "- **یادداشت‌ها:** همه، برچسب، بایگانی و سطل زباله. رنگ، چک‌لیست، عکس و سنجاق.",
    "- **CRM:** فهرست و پرونده‌ی مشتری (نماینده‌ها، تلفن‌ها، مشخصات)، برچسب‌ها، ثبت تماس، نامه‌های مشتری،",
    "  ورود مشتری از فایل و گزارش چاپی.",
    "- **فروش:** فرصت‌ها (مراحل احتمال، ارزش وزنی)، پرداخت‌ها (سند پرداختی)، و مانیتورینگ فروش و پرداخت.",
    "- **صورتجلسه (ساده و پیشرفته):** اطلاعات، اعضا (مجری و ناظر)، حضور و غیاب، یادداشت، وظایف، نظرها،",
    "  پیامک به اعضا، امضا، قالب و یادآوری.",
    "- **نظرسنجی:** ساخت (ناشناس، چند پاسخ، آزمونی، قالب)، رأی دادن و پس گرفتن رأی، نتایج، چاپ و توقف.",
    "- **جلسه‌ی تصویری:** شروع، اعضا، وضعیت میکروفون و تصویر، و درخواست‌های در انتظار.",
    "- **حضور و غیاب:** شروع و پایان، و تاریخچه‌ی آنلاین و دستی.",
    "- **مانیتورینگ:** میزکار، کاربران، کاربر، وظایف کاربر، مشتریان، صورتجلسه‌ها، پروژه‌ها و تقویم پروژه‌ها.",
    "- **جستجو و نشان‌شده‌ها:** جستجو در همه‌ی محتوا با فیلتر.",
    "- **تنظیمات میزکار:** عمومی، اعضا، اعضای حذف‌شده، دعوت، مجوزها (سازندگان پروژه، گروه و CRM، و نقش‌ها) و مالی (طرح، خرید، کد تخفیف).",
    "- **دیگر:** پشتیبانی آنلاین (همراه ارزیابی کیفیت)، چاپ، ابزار اصلاح داده (مدیر) و تاریخچه‌ی اعلان‌ها.",
    "",
    "## پوشش MCP",
    "",
    "وضعیت هر endpoint در [api.md](api.md) آمده است:",
    "",
    "| وضعیت | تعداد |",
    "|---|---|",
] + [f"| {k} | {v} |" for k, v in sorted(status_count.items())] + [""]
(OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

site_map = {
    "generated": date.today().isoformat(),
    "states": states,
    "views": VIEWS,
    "template_contexts": MAP["templates"],
    "endpoints": {ep: {**MAP["endpoints"][ep], "mcp_status": rows_all[ep][0], "mcp_note": rows_all[ep][1],
                       "mcp_functions": sorted(mcp_use.get(ep, set()))} for ep in MAP["endpoints"]},
    "other_http": {"raw": MAP["raw_http"], "capi": MAP["capi"], "form_posts": MAP["form_posts"]},
    "realtime": {"out_workspace_events": EVENTS["out_workspace_events"],
                 "listened_not_broadcast": EVENTS["server_pushed_candidates"],
                 "on_event_counts": EVENTS["on_event_counts"]},
    "message_media_types": EXTRA["media_types"], "message_action_types": EXTRA["action_types"],
    "plan_options": MAP["plan_options"], "access_flags": access_real, "config_keys": MAP["config_keys"],
    "local_storage": MAP["local_storage"], "state_go_targets": EXTRA["state_go_targets"],
    "settings_pages": EXTRA["settings_pages"], "modules": MAP["modules"], "i18n": MAP["i18n"],
    "js_persian_strings": JS_STRINGS,
}
(OUT / "site_map.json").write_text(json.dumps(site_map, ensure_ascii=False, indent=1), encoding="utf-8")
print({f.name: f.stat().st_size for f in sorted(OUT.iterdir())})
print(dict(status_count))

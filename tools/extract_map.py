"""Phase 1 of the Mizito site map: exhaustive static extraction from the web client bundle.
Writes /tmp/mizito_map.json."""
import bisect
import json
import re

T = open("/tmp/mizito_a.js", encoding="utf-8", errors="replace").read()


def match_brace(text, start, open_ch="{", close_ch="}", limit=200000):
    depth, i = 0, start
    in_str = None
    while i < len(text) and i < start + limit:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
        elif ch in "\"'`":
            in_str = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def decode(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s


# ---- angular modules (services, controllers, ...) -------------------------------------------------
modules = []
for m in re.finditer(r"\b(?:app|angular\.module\([^)]*\))\.(service|factory|controller|directive|filter|component|constant|provider)\(\"([^\"]+)\"", T):
    modules.append({"kind": m.group(1), "name": m.group(2), "pos": m.start()})
modules.sort(key=lambda x: x["pos"])
mod_pos = [m["pos"] for m in modules]


def module_at(pos):
    i = bisect.bisect_right(mod_pos, pos) - 1
    return f'{modules[i]["kind"]}:{modules[i]["name"]}' if i >= 0 else "(top-level)"


FUNC = re.compile(r"(?:([A-Za-z_$][\w$]{2,})\s*:\s*(?:async\s+)?function|\.([A-Za-z_$][\w$]{2,})\s*=\s*(?:async\s+)?function|function\s+([A-Za-z_$][\w$]{2,})\s*\()")


def function_at(pos):
    window = T[max(0, pos - 6000):pos]
    names = [next(g for g in m.groups() if g) for m in FUNC.finditer(window)]
    return names[-1] if names else None


# ---- ui-router states --------------------------------------------------------------------------
states = []
for m in re.finditer(r"\.state\(\"([^\"]+)\",\{", T):
    end = match_brace(T, m.end() - 1)
    body = T[m.end() - 1:end + 1]
    url = re.search(r"url:\"([^\"]*)\"", body)
    tpl = re.search(r"templateUrl:templateUrl\(\"([^\"]+)\"\)", body) or re.search(r"templateUrl:\"([^\"]+)\"", body)
    ctrl = re.search(r"controller:\"([^\"]+)\"", body)
    params = re.search(r"params:\{([^}]*)\}", body)
    states.append({
        "name": m.group(1),
        "url": url.group(1) if url else None,
        "template": tpl.group(1) if tpl else None,
        "controller": ctrl.group(1) if ctrl else None,
        "abstract": "abstract:!0" in body,
        "params": re.findall(r"([A-Za-z_]\w*):", params.group(1)) if params else [],
        "redirect": (re.search(r"redirectTo:\"([^\"]+)\"", body) or [None, None])[1],
    })

# ---- templates -----------------------------------------------------------------------------------
templates = {}
for m in re.finditer(r"templateUrl\(\"([^\"]+)\"\)", T):
    ctx = T[max(0, m.start() - 400):m.start()]
    kind = "state" if ".state(" in ctx[-200:] else "modal/panel" if re.search(r"\.show\(\{|controller:", ctx[-250:]) else "directive/other"
    templates.setdefault(m.group(1), {"uses": 0, "contexts": set()})
    templates[m.group(1)]["uses"] += 1
    templates[m.group(1)]["contexts"].add(f"{module_at(m.start())} / {function_at(m.start())} / {kind}")
dynamic_templates = [T[max(0, m.start() - 160):m.end() + 60] for m in re.finditer(r"templateUrl\([^\"\)][^\)]{0,40}\)", T)]

# ---- endpoints -------------------------------------------------------------------------------------
endpoints = {}
for m in re.finditer(r"invokeApi\(", T):
    i, depth, arg = m.end(), 0, []
    while i < len(T) and i < m.end() + 400:
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
    names = re.findall(r"[\"']([A-Za-z][A-Za-z0-9_]*\.[A-Za-z0-9_.]+)[\"']", "".join(arg))
    if not names:
        continue
    sig = "-"
    j = i
    if j < len(T) and T[j] == ",":
        j += 1
        while T[j] == " ":
            j += 1
        if T[j] == "{":
            k = match_brace(T, j, limit=4000)
            body, top, dd = T[j + 1:k], [], 0
            for ch in body:
                if ch in "{[(":
                    dd += 1
                elif ch in "}])":
                    dd -= 1
                elif dd == 0:
                    top.append(ch)
                if dd > 0 and (not top or top[-1] != "~"):
                    top.append("~")
            keys = re.findall(r"(?:^|,)\s*[\"']?([A-Za-z_$][\w$]*)[\"']?\s*:", "".join(top))
            sig = ",".join(keys) or "{}"
        else:
            v = re.match(r"[\w$.]+", T[j:j + 40])
            sig = "var:" + (v.group(0) if v else "?")
    site = {"module": module_at(m.start()), "function": function_at(m.start())}
    for n in names:
        e = endpoints.setdefault(n, {"params": set(), "sites": []})
        e["params"].add(sig)
        if site not in e["sites"]:
            e["sites"].append(site)

# ---- endpoints reached through wrappers (y("..."), w("...")) or ternaries stored in variables ------
MODS = sorted({e.split(".")[0] for e in endpoints})
INDIRECT = re.compile(r"(\$watch\(|[(?:])\s*\"((?:" + "|".join(MODS) + r")\.[a-z][A-Za-z]{2,}(?:\.[a-z][A-Za-z]{2,})*)\"(?=\s*([),:]))")
for m in INDIRECT.finditer(T):
    if m.group(1) == "$watch(" or m.group(2) in endpoints:
        continue
    sig = "-"
    if m.group(3) == ",":
        j = m.end()
        while T[j] in " ,":
            j += 1
        if T[j] == "{":
            k = match_brace(T, j, limit=4000)
            keys = re.findall(r"(?:^|,)\s*([A-Za-z_$][\w$]*)\s*:", re.sub(r"\{[^{}]*\}|\[[^\[\]]*\]", "~", T[j + 1:k]))
            sig = ",".join(keys) or "{}"
        else:
            v = re.match(r"[\w$.]+", T[j:j + 40])
            sig = "var:" + (v.group(0) if v else "?")
    e = endpoints.setdefault(m.group(2), {"params": set(), "sites": [], "indirect": True})
    e["params"].add(sig)
    site = {"module": module_at(m.start()), "function": function_at(m.start())}
    if site not in e["sites"]:
        e["sites"].append(site)

# ---- other network calls -------------------------------------------------------------------------
raw_http = sorted(set(re.findall(r"Config\.App\.(\w+)\+\"(/[^\"]+)\"", T)))
capi = sorted(set(re.findall(r"\"/capi/([^\"]*)\"", T)))
config_keys = sorted(set(re.findall(r"Config\.App\.([A-Za-z_]\w*)", T)))
http_direct = []
for m in re.finditer(r"\b[a-z]\(\{method:\"(GET|POST|PUT|DELETE)\",url:([^,}]{1,120})", T):
    http_direct.append({"method": m.group(1), "url": m.group(2), "module": module_at(m.start()), "function": function_at(m.start())})
form_posts = sorted(set(re.findall(r"\.action=Config\.App\.(\w+)\+\"([^\"]+)\"", T)))

# ---- realtime (socket.io) ------------------------------------------------------------------------
DOM = {"click", "keydown", "keyup", "keypress", "change", "input", "focus", "blur", "scroll", "resize", "load", "error",
       "mousedown", "mouseup", "mousemove", "mouseenter", "mouseleave", "mouseover", "mouseout", "touchstart", "touchend",
       "touchmove", "paste", "drop", "dragover", "dragenter", "dragleave", "dragstart", "dragend", "submit", "contextmenu",
       "wheel", "dblclick", "unload", "beforeunload", "visibilitychange", "message", "open", "close", "online", "offline",
       "hashchange", "popstate", "select", "copy", "cut", "transitionend", "animationend", "loadedmetadata", "ended",
       "play", "pause", "timeupdate", "canplay", "shown", "hidden", "show", "hide", "success", "progress", "abort"}
socket_on = sorted({n for n in re.findall(r"\.on\(\"([A-Za-z_:.\-]+)\"", T) if n not in DOM and not n.startswith(("md", "jq"))})
socket_emit = sorted(set(re.findall(r"\.emit\(\"([A-Za-z_:.\-]+)\"", T)))
socket_ctx = [T[max(0, m.start() - 200):m.start() + 300] for m in re.finditer(r"\bio\(|io\.connect\(", T)]

# ---- plans, access, storage, i18n ---------------------------------------------------------------
plan_options = sorted(set(re.findall(r"checkPlanOption\([^,\"]{0,40},\"([^\"]+)\"", T)) | set(re.findall(r"\"([a-z_]+::[a-z_:]+)\"", T)))
access_flags = sorted(set(re.findall(r"\b(access_[a-z_]+)\b", T)))
storage = sorted(set(re.findall(r"localStorage\.(?!getItem|setItem|removeItem|clear|key|length)([A-Za-z_]\w*)", T))
                 | set(re.findall(r"localStorage\.(?:getItem|setItem|removeItem)\(\"([^\"]+)\"", T))
                 | set(re.findall(r"localStorage\[\"([^\"]+)\"", T)))
i18n = {}
for m in re.finditer(r"(?:[{,])([a-z][a-z0-9_]{2,}):\"((?:[^\"\\]|\\.)*)\"", T):  # linear: no overlapping branches
    val = m.group(2)
    if "\\u06" in val and m.group(1) not in i18n:
        i18n[m.group(1)] = decode(val)

out = {
    "states": states,
    "templates": {k: {"uses": v["uses"], "contexts": sorted(v["contexts"])} for k, v in sorted(templates.items())},
    "dynamic_templates": dynamic_templates,
    "modules": [{k: m[k] for k in ("kind", "name")} for m in modules],
    "endpoints": {k: {"params": sorted(v["params"]), "sites": v["sites"], "indirect": v.get("indirect", False)} for k, v in sorted(endpoints.items())},
    "raw_http": raw_http, "capi": capi, "http_direct": http_direct, "form_posts": form_posts, "config_keys": config_keys,
    "socket_on": socket_on, "socket_emit": socket_emit, "socket_ctx": socket_ctx,
    "plan_options": plan_options, "access_flags": access_flags, "local_storage": storage, "i18n": i18n,
}
json.dump(out, open("/tmp/mizito_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in out.items()})

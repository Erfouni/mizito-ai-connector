"""Blind-spot scan: API names that reach the network without a literal inside invokeApi(...)."""
import json
import re

T = open("/tmp/mizito_a.js", encoding="utf-8", errors="replace").read()
known = set(json.load(open("/tmp/mizito_map.json", encoding="utf-8"))["endpoints"])
modules = sorted({e.split(".")[0] for e in known})
mod_re = "|".join(modules)
PERSIAN = re.compile(r"(?:\\u[0-9A-Fa-f]{4})+")

# 1) invokeApi called with a variable as the endpoint name
var_calls = []
for m in re.finditer(r"invokeApi\(\s*([A-Za-z_$][\w$.]*)\s*[,)]", T):
    var_calls.append(PERSIAN.sub("·", T[max(0, m.start() - 260):m.end() + 60]))

# 2) any string literal shaped like "<known module>.<method>" anywhere in the bundle
all_literals = set(re.findall(r"[\"'](" + mod_re + r")\.([A-Za-z][\w.]*)[\"']", T))
literal_names = {f"{a}.{b}" for a, b in all_literals}
unknown = sorted(n for n in literal_names - known if not re.search(r"\.(js|css|html|png|svg|json)$", n))
unknown_ctx = {}
for n in unknown:
    m = re.search(r"[\"']" + re.escape(n) + r"[\"']", T)
    unknown_ctx[n] = PERSIAN.sub("·", T[max(0, m.start() - 160):m.end() + 80]) if m else ""

json.dump({"var_calls": var_calls, "unknown_literals": unknown_ctx}, open("/tmp/mizito_blindspots.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print({"invokeApi_with_variable": len(var_calls), "module_method_literals_not_in_map": len(unknown)})

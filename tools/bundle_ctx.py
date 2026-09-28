"""Print code context around regex matches in the Mizito web bundle.
usage: python3 bundle_ctx.py LABEL::REGEX::BEFORE::AFTER [...]"""
import re
import sys

text = open("/tmp/mizito_a.js", encoding="utf-8", errors="replace").read()
persian = re.compile(r"(?:\\u[0-9A-Fa-f]{4})+")

for spec in sys.argv[1:]:
    label, pattern, before, after = spec.split("::")
    matches = list(re.finditer(pattern, text))
    print(f"====== {label} ({len(matches)})")
    for m in matches[:1]:
        chunk = text[max(0, m.start() - int(before)): m.start() + int(after)].replace("\n", " ")
        print(persian.sub("·", chunk))
    print()

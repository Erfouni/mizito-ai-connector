"""Every Persian string literal in the deobfuscated bundle (toasts, dialogs, labels built in code).
usage: python tools/extract_js_strings.py <deobfuscated.js> <out.json>"""
import json
import re
import sys

T = open(sys.argv[1], encoding="utf-8", errors="replace").read()
strings = set()
for m in re.finditer(r"\"((?:[^\"\\\n]|\\.){2,400})\"|'((?:[^'\\\n]|\\.){2,400})'", T):
    s = m.group(1) if m.group(1) is not None else m.group(2)
    if not re.search(r"[؀-ۿ]", s) or re.search(r"<[a-z][^>]*>", s):
        continue
    try:
        s = json.loads("\"" + s.replace("\\'", "'") + "\"") if "\\" in s else s
    except Exception:
        pass
    s = re.sub(r"\s+", " ", s).strip()
    if s:
        strings.add(s)
json.dump(sorted(strings), open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({"persian_js_strings": len(strings)})

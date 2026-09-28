# ابزارهای ساخت نقشه‌ی سایت

اسکریپت‌هایی که [docs/site-map](../docs/site-map/README.md) را از روی کد وب‌اپ میزیتو می‌سازند.

1. روی سروری که به `office.mizito.ir` دسترسی دارد، `a_.js` را در `/tmp/mizito_a.js` بگذارید:
   `curl -s --compressed -o /tmp/mizito_a.js https://office.mizito.ir/a_.js`.
   بعد به ترتیب این‌ها را اجرا کنید: `extract_map.py`، `extract_realtime.py`، `extract_events.py`، `extract_templates.py`
   (هر کدام یک فایل `/tmp/mizito_*.json` می‌سازد).
2. کد را رمزگشایی کنید:
   `npx -y webcrack@2.16.0 a_.js -o out`. خروجی اصلی `out/deobfuscated.js` است.
3. روی کد رمزگشایی‌شده این‌ها را اجرا کنید:
   - `extract_deobfuscated.py`: endpoint، صفحه و ارجاع قالبی که فقط داخل کد مبهم‌شده بوده است.
   - `extract_embedded_views.py`: قالب‌هایی که با `my-include` بار می‌شوند.
   - `extract_inline_html.py`
   - `extract_js_strings.py`
4. قالب‌ها را یکی کنید: `merge_views.py`. خروجی این مرحله نباید هیچ include حل‌نشده‌ای داشته باشد.
5. `diff_inline_vs_views.py` را اجرا کنید. نباید هیچ `ng-click` یا `ng-model`ی خارج از نقشه بماند.
6. بعد:
   - `extract_blindspots.py`: فراخوانی‌هایی که اسم endpoint در آن‌ها از متغیر می‌آید.
   - `build_site_map.py <پوشه‌ی json‌ها>`
   - `check_site_map.py`: باید `problems: 0` بدهد.

`bundle_ctx.py` برای دیدن کد اطراف یک الگو در `a_.js` است.

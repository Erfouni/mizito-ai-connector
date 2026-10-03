# تغییرات · Changelog

## v0.3.1 · ۱۱ مهر ۱۴۰۵ (2026-10-03)

<div dir="rtl">

- **نوع پلن میزکار:** `mizito_whoami` و `mizito_workspace_info` حالا می‌گویند پلن «پایه» است یا «پیشرفته». پروژه‌ی پیشرفته، گانت، الگوی وظیفه، اتوماسیون و صورتجلسه‌ی پیشرفته فقط در پلن پیشرفته هستند. خطای این قابلیت‌ها هم علت را دقیق می‌گوید: میزکار پلن پایه دارد و دسترسی مدیر این را عوض نمی‌کند.

</div>

- **Workspace plan type:** `mizito_whoami` and `mizito_workspace_info` now say whether the plan is basic (پایه) or advanced (پیشرفته). Advanced projects, Gantt, task templates, automation and advanced minutes exist only on the advanced plan, and their errors now state the cause: the workspace has the basic plan, and admin rights do not change that.

## v0.3.0 · ۱۱ مهر ۱۴۰۵ (2026-10-03)

<div dir="rtl">

- **نصب با یک دستور، بدون git:** `curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | bash`. کد را خودش دانلود می‌کند، فقط دامنه و نام کاربری و رمز میزیتو را می‌پرسد و IP سرور را برای ساختن رکورد DNS نشان می‌دهد. راهنمای [SETUP.md](SETUP.md) کوتاه شد: سه قدم.
- **ورود ساده‌تر:** دیگر لازم نیست توکن را از Console مرورگر دربیاورید. نام کاربری و رمز همان لحظه بررسی می‌شوند و اگر اشتباه باشند دوباره پرسیده می‌شوند. برای ورود دومرحله‌ای، کد پیامکی را می‌پرسد. رقم‌های فارسی و شماره‌ی موبایل را مثل فرم ورود وب میزیتو می‌پذیرد.
- **دستور `mizito-connector`** روی سرور، از هر پوشه‌ای: `url`، `status`، `login`، `update` و `logs`.
- **پیام روشن برای خطاهای رایج:** دامنه‌ای که به سرور اشاره نمی‌کند، ابر نارنجی Cloudflare، پورت 80 یا 443 اشغال، و نبودن دسترسی به Let's Encrypt یا pypi.org. اگر pypi.org باز نباشد، بسته‌ها از mirrorهای ایرانی نصب می‌شوند و hash هر فایل باز هم بررسی می‌شود.
- **ایمنی ورود خودکار:** اگر میزیتو رمز ذخیره‌شده را رد کند، سرور تا ری‌استارت بعدی دوباره امتحانش نمی‌کند، تا حساب قفل نشود و پیامک پشت سر هم نیاید.
- دستور قدیمی `sudo bash deploy/install.sh` همچنان کار می‌کند.

</div>

- **One-command install, no git:** `curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | bash`. It downloads the code itself, asks only for the domain and the Mizito username and password, and shows the server's IP for the DNS record. [SETUP.md](SETUP.md) is now three short steps.
- **Easier login:** no more copying a token from the browser console. The username and password are checked right away and asked again when wrong; with two-step login it asks for the SMS code. Persian digits and mobile numbers are read the way Mizito's web login form reads them.
- **The `mizito-connector` command** on the server, from any folder: `url`, `status`, `login`, `update` and `logs`.
- **Clear messages for the usual problems:** a domain that does not point to the server, Cloudflare's orange cloud, ports 80/443 in use, and no access to Let's Encrypt or pypi.org. When pypi.org is blocked, packages come from Iranian mirrors, still checked against their hashes.
- **Safer automatic login:** when Mizito refuses the saved password, the server does not retry it until the next restart, so the account is not locked and no SMS codes pile up.
- The old `sudo bash deploy/install.sh` still works.

## v0.2.0 · ۸ مهر ۱۴۰۵ (2026-09-30)

<div dir="rtl">

- **۱۰۵ ابزار** (قبلاً ۴۸): نظرسنجی، صورتجلسه (ساده و پیشرفته)، گانت، مدیریت ستون‌های کانبان، وظایف تکراری، الگوی وظیفه، ویرایش و حذف گزارش وظیفه، حضور و غیاب، گزارش‌های مانیتورینگ، اتوماسیون و فرم‌های درخواست، CRM، مدیریت میزکار و پشتیبانی میزیتو.
- **فایل‌ها:** خواندن متن PDF، Word، Excel و PowerPoint؛ دیدن عکس (مثلاً نامه‌ی اسکن‌شده)؛ لینک دانلود؛ آپلود فایل و پیوست کردنش به پیام، نامه، وظیفه و صورتجلسه.
- **نامه‌ها:** جستجو با فیلتر، پاراف (ارجاع)، اتصال به گفتگو، حذف با تأیید، و ثبت در دبیرخانه.
- **توضیح کامل هر ابزار:** عنوان فارسی، توضیح کامل برای هوش مصنوعی، توضیح هر پارامتر و یک راهنمای کلی. فهرست همه‌ی ابزارها در [docs/TOOLS.md](docs/TOOLS.md) است.
- **تاریخ شمسی:** تاریخ‌ها را می‌شود شمسی داد و خروجی‌ها کنار هر تاریخ معادل شمسی‌اش را هم دارند.
- **ایمنی:** حذف برگشت‌ناپذیر فقط با تکرار عنوان دقیق مورد انجام می‌شود. کلید فایل‌ها و توکن وظیفه‌ها هرگز از سرور بیرون نمی‌رود.
- **نصب با یک دستور:** `sudo bash deploy/install.sh` فقط دامنه و حساب میزیتو را می‌پرسد. راهنمای ساده‌ی دوزبانه در [SETUP.md](SETUP.md) است.
- **ورود با نام کاربری و رمز** تست شد. با آن سرور خودش نشست را تمدید می‌کند. برای امتحانش: `check_login.py`.
- لایسنس MIT.

</div>

- **105 tools** (up from 48): polls, meeting minutes (simple and advanced), Gantt, kanban board management, recurring tasks, task templates, editing and deleting task comments, attendance, monitoring reports, automation and request forms, CRM, workspace admin, and Mizito support.
- **Files:** read the text of PDF, Word, Excel and PowerPoint files; view images (e.g. scanned letters); download links; upload files and attach them to messages, letters, tasks and minutes.
- **Letters:** search with filters, referral (پاراف), linking to conversations, deletion with confirmation, and secretariat registration.
- **Full tool descriptions:** a Persian title, a full description for the AI, per-parameter descriptions and server instructions. Every tool is listed in [docs/TOOLS.md](docs/TOOLS.md).
- **Jalali dates:** accepted as input, and shown next to every date in results.
- **Safety:** an irreversible deletion needs the item's exact title as confirmation. File access keys and task tokens never leave the server.
- **One-command install:** `sudo bash deploy/install.sh` asks only for a domain and the Mizito login. [SETUP.md](SETUP.md) is a simple Persian/English guide.
- **Username + password login** is tested and lets the server renew its session by itself. Test it with `check_login.py`.
- MIT license.

## v0.1.0 · ۶ مهر ۱۴۰۵ (2026-09-28)

<div dir="rtl">

- اولین نسخه با **۴۸ ابزار**:
  - خواندن گفتگوها، پروژه‌ها، وظایف، تقویم، نامه‌ها و یادداشت‌ها.
  - ارسال پیام و نامه.
  - ساخت و ویرایش وظیفه و پروژه، یادآوری و رویداد تقویم.
- اجرای سرور روی HTTPS برای Claude.ai و ChatGPT.

</div>

- First version with **48 tools**:
  - Read chats, projects, tasks, calendar, letters and notes.
  - Send messages and letters.
  - Create and edit tasks and projects, reminders and calendar events.
- Remote HTTPS server for Claude.ai and ChatGPT.

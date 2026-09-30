# تغییرات · Changelog

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

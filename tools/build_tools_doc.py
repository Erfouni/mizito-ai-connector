"""Generate docs/TOOLS.md, the Persian reference of every MCP tool, from the tool definitions themselves.
usage: uv run python tools/build_tools_doc.py"""
from __future__ import annotations

import asyncio
import importlib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.update(MIZITO_ENABLE_WRITE="1", MIZITO_ENABLE_CRM="1", MIZITO_ENABLE_ADMIN="1")  # document everything

import mizito  # noqa: E402
from mizito.app import TOOL_INFO, mcp  # noqa: E402

for module in mizito.MODULES:
    importlib.import_module(f"mizito.{module}")

SECTIONS = {
    "account": "حساب و میزکار", "chat": "گفتگو و پیام", "meetings": "نظرسنجی و صورتجلسه",
    "projects": "پروژه‌ها و ستون‌های کانبان", "tasks": "وظایف و تقویم", "gantt": "نمودار گانت",
    "letters": "نامه‌ها و دبیرخانه", "notes": "یادداشت‌ها و برچسب‌ها", "files": "فایل‌ها",
    "attendance": "حضور و غیاب", "reports": "گزارش‌ها و مانیتورینگ", "automation": "اتوماسیون و فرم‌های درخواست",
    "crm": "CRM: مشتریان، فروش و اسناد مالی", "admin": "مدیریت میزکار", "support": "پشتیبانی میزیتو",
    "raw": "دسترسی مستقیم",
}
KIND_FA = {"read": "خواندنی", "create": "ساختن", "set": "تنظیم", "update": "تغییر", "delete": "حذف"}
FEATURE_FA = {None: "", "crm": "`MIZITO_ENABLE_CRM=1`", "admin": "`MIZITO_ENABLE_ADMIN=1`"}

FA = {
    "mizito_whoami": "کاربر واردشده، میزکار فعال و میزکارهای دیگر، نقش (مدیر یا مهمان) و مجوز ساخت پروژه، گروه و پرونده‌ی مشتری.",
    "mizito_switch_workspace": "عوض کردن میزکار فعال؛ بعد از آن همه‌ی ابزارها روی میزکار جدید کار می‌کنند.",
    "mizito_dashboard": "شمارنده‌های داشبورد برای هر میزکار: نامه و پیام خوانده‌نشده، کارهای امروز و عقب‌افتاده.",
    "mizito_list_users": "اعضای میزکار با شناسه، نقش، سمت و آخرین بازدید. شناسه‌ها برای مسئول، گیرنده و عضو لازم‌اند.",
    "mizito_workspace_info": "نام میزکار، وضعیت پلن، مجوزهای شما، دعوت‌های در انتظار از میزکارهای دیگر و شمارنده‌ها.",
    "mizito_respond_workspace_invitation": "پذیرفتن یا رد کردن دعوت به یک میزکار دیگر.",
    "mizito_invite_workspace_member": "دعوت فرد جدید به میزکار با ایمیل یا شماره موبایل (شاید دسترسی مدیر لازم باشد).",
    "mizito_set_presence": "متن وضعیت کنار اسم شما و حالت «مزاحم نشوید» (قطع اعلان‌ها برای چند ساعت).",
    "mizito_list_conversations": "فهرست گفتگوها (خصوصی، گروه، پروژه، مشتری) با تعداد خوانده‌نشده، به ترتیب آخرین فعالیت.",
    "mizito_get_messages": "پیام‌های یک گفتگو (تا ۶۰۰ پیام در هر بار)، صفحه‌به‌صفحه یا از یک تاریخ و ساعت مشخص؛ همراه با فایل‌ها، وظیفه‌ها، نظرسنجی‌ها و صورتجلسه‌ها.",
    "mizito_search_messages": "جستجوی متنی در همه‌ی پیام‌های میزکار یا پرونده‌های مشتری.",
    "mizito_get_message_info": "چه کسی و کِی یک پیام را دیده، و آیا هنوز قابل ویرایش یا حذف است.",
    "mizito_get_conversation": "جزئیات یک گفتگو: نوع، اعضا و مدیران، بی‌صدا بودن، پروژه‌ی مرتبط و وظایف باز.",
    "mizito_send_message": "ارسال پیام، با امکان پاسخ به یک پیام و پیوست فایل.",
    "mizito_start_conversation": "باز کردن یا ساختن گفتگوی خصوصی با یک عضو.",
    "mizito_mark_conversation_read": "علامت خوانده‌شده برای همه‌ی پیام‌های یک گفتگو.",
    "mizito_manage_message": "ویرایش یا حذف پیام خودتان، حذف پیام دیگران توسط مدیر گروه، سنجاق، نشان کردن و مدیریت منشن‌ها.",
    "mizito_manage_conversation": "سنجاق و بی‌صدا کردن گفتگو، تغییر نام گروه، افزودن و حذف عضو، مدیر کردن، عادی کردن گروه عمومی، حذف عکس و حذف کامل گروه (با تأیید).",
    "mizito_create_group": "ساخت گروه گفتگو با اعضای مشخص.",
    "mizito_create_poll": "ساخت نظرسنجی در گفتگو: چند سؤالی، چند گزینه‌ای، مسابقه‌ای، عمومی یا محرمانه.",
    "mizito_get_poll_results": "نتیجه‌ی نظرسنجی: تعداد و درصد رأی هر گزینه، رأی‌دهندگان (اگر قابل دیدن باشد) و رأی خودتان.",
    "mizito_poll_action": "رأی دادن، پس گرفتن رأی، پایان دادن به نظرسنجی و ذخیره‌ی آن به‌عنوان الگو.",
    "mizito_create_minute": "ثبت صورتجلسه در گفتگو با موضوع، تاریخ، مکان، متن، مصوبات (که وظیفه می‌شوند) و پیوست.",
    "mizito_get_minute": "صورتجلسه‌ی کامل (ساده یا پیشرفته) با وظایف، فایل‌ها، حضور و سابقه‌ی تغییرات.",
    "mizito_manage_minute": "ویرایش صورتجلسه‌ی ساده یا تبدیل آن به الگو.",
    "mizito_create_advanced_minute": "پیش‌نویس صورتجلسه‌ی پیشرفته (دعوت، حضور و غیاب، امضا) در پروژه‌ی پیشرفته.",
    "mizito_manage_advanced_minute": "گردش کار صورتجلسه‌ی پیشرفته: ارسال دعوت، نوشتن متن، ارسال برای امضا، امضا، نظر و پیامک.",
    "mizito_list_templates": "الگوهای صورتجلسه، صورتجلسه‌ی پیشرفته، نظرسنجی و وظیفه‌ی پروژه.",
    "mizito_list_projects": "فهرست پروژه‌ها با رنگ، اعضا و اینکه در تب پروژه‌ها دیده می‌شوند یا نه.",
    "mizito_get_project": "نمای کامل یک پروژه: اعضا و مدیران، ستون‌ها با آمار هر ستون، برچسب‌ها، گفتگوی پروژه، امکانات پیشرفته و آمار وظایف.",
    "mizito_create_project": "ساخت پروژه دقیقاً مثل دکمه‌ی «ایجاد پروژه» وب: پروژه به‌همراه گفتگوی پروژه.",
    "mizito_update_project": "تغییر نام، رنگ، اعضا و برچسب‌های پروژه.",
    "mizito_add_project_members": "افزودن عضو به پروژه.",
    "mizito_add_project_board": "افزودن ستون (لیست) کانبان به پروژه.",
    "mizito_manage_project_board": "تغییر نام، رنگ و ترتیب ستون، مرتب کردن وظایف ستون، و حذف ستون خالی.",
    "mizito_archive_project": "آرشیو پروژه، با یا بدون وظایفش.",
    "mizito_clone_project": "کپی گرفتن از پروژه با ستون‌ها و وظایف.",
    "mizito_set_project_advanced": "روشن کردن پروژه‌ی پیشرفته و امکاناتش: گانت، اتوماسیون، صورتجلسه‌ی پیشرفته، وزن وظایف، تأیید مدیر و غیره.",
    "mizito_list_project_files": "همه‌ی فایل‌های پیوست‌شده در گفتگو و وظایف یک پروژه.",
    "mizito_list_tasks": "وظایف: کارهای من، پیگیری از دیگران، وظایف یک پروژه و انجام‌شده‌ها.",
    "mizito_get_task": "جزئیات کامل وظیفه با تاریخ‌های شمسی، چک‌لیست، تکرار، تأییدکننده‌ها و فایل‌ها.",
    "mizito_get_task_comments": "گزارش‌های (کامنت‌های) وظیفه با فایل‌ها و پاسخ‌ها.",
    "mizito_get_task_extras": "چه کسی وظیفه را ساخته و دیده، جایگاهش در گانت، دکمه‌های اتوماسیون و گردش کار.",
    "mizito_calendar": "تقویم یک ماه شمسی (خودتان یا یک پروژه) بر اساس زمان یادآوری.",
    "mizito_get_history": "سابقه‌ی تغییرات یک وظیفه یا پروژه.",
    "mizito_create_task": "ساخت وظیفه با همه‌ی امکانات فرم وب: مسئولان، شروع، مهلت، یادآوری، تکرار، چک‌لیست، ستون، برچسب، تأییدکننده، وزن، فایل و الگو.",
    "mizito_create_calendar_event": "افزودن رویداد به تقویم (وظیفه‌ای با زمان شروع و پایان، قابل تکرار).",
    "mizito_update_task": "ویرایش وظیفه: عنوان، توضیح، مسئولان، برچسب، پروژه، ستون، شروع، مهلت، تأییدکننده، وزن، چک‌لیست و فایل.",
    "mizito_comment_on_task": "ثبت گزارش روی وظیفه، با پاسخ، منشن و فایل.",
    "mizito_manage_task_comment": "ویرایش یا حذف گزارش خودتان، تا وقتی دیگران آن را ندیده‌اند.",
    "mizito_set_task_completed": "انجام‌شده کردن یا بازگشایی وظیفه.",
    "mizito_set_task_deadline": "تعیین یا حذف مهلت وظیفه.",
    "mizito_set_task_progress": "درصد پیشرفت وظیفه.",
    "mizito_set_task_reminder": "زمان یادآوری وظیفه، یعنی گذاشتن آن در تقویم.",
    "mizito_set_task_repeat": "تکرار وظیفه: روزانه، هفتگی در روزهای مشخص، ماهانه، سالانه و...، تا یک تاریخ یا چند بار.",
    "mizito_check_task_item": "تیک زدن آیتم چک‌لیست.",
    "mizito_move_task_to_board": "جابه‌جا کردن وظیفه بین ستون‌های کانبان.",
    "mizito_manage_task": "نشان کردن، حذف و بازگردانی، لغو پیگیری، حذف از بورد و ساخت لینک اشتراک وظیفه.",
    "mizito_manage_task_template": "ساخت، ویرایش و حذف الگوی وظیفه‌ی پروژه.",
    "mizito_get_gantt": "نمودار گانت پروژه: فازها، شروع و پایان وظایف و وابستگی‌ها.",
    "mizito_manage_gantt": "ویرایش گانت: ساخت، تغییر نام و حذف فاز، افزودن و جابه‌جایی وظایف، زمان‌بندی و وابستگی.",
    "mizito_list_letters": "فهرست و جستجوی نامه‌ها (ورودی، خروجی، آرشیو) با فیلتر فرستنده، گیرنده، خوانده‌شده، پیوست، برچسب و شماره‌ی دبیرخانه.",
    "mizito_get_letter_thread": "متن کامل یک رشته نامه با پاسخ‌ها و پاراف‌ها، فایل‌ها، برچسب‌ها و اینکه چه کسی خوانده.",
    "mizito_send_letter": "ارسال نامه‌ی جدید با پیوست و برچسب.",
    "mizito_reply_letter": "پاسخ در رشته نامه، یا پاراف (ارجاع) آن به افراد دیگر.",
    "mizito_manage_letter": "آرشیو، نشان، خوانده‌شده، برچسب، اتصال به گفتگو یا پرونده‌ی مشتری، و حذف (با تأیید).",
    "mizito_register_letter": "ثبت نامه در دبیرخانه با شماره‌ی رسمی (وارده یا صادره).",
    "mizito_list_notes": "یادداشت‌های شخصی، فعال یا آرشیوشده.",
    "mizito_create_note": "ساخت یادداشت با رنگ، چک‌لیست و برچسب.",
    "mizito_update_note": "ویرایش یادداشت: عنوان، متن، رنگ، برچسب و افزودن به چک‌لیست.",
    "mizito_manage_note": "آرشیو، سنجاق، حذف و بازگردانی یادداشت، و تیک چک‌لیست.",
    "mizito_list_labels": "برچسب‌های هر نوع: وظیفه، نامه، یادداشت، پروژه، مشتری، معامله، سند مالی و صورتجلسه.",
    "mizito_create_label": "ساخت برچسب.",
    "mizito_manage_label": "تغییر نام و رنگ برچسب، سابقه‌ی آن و حذف (با تأیید).",
    "mizito_read_file": "خواندن متن فایل پیوست: PDF، Word، Excel، PowerPoint، متن، CSV و HTML.",
    "mizito_view_image": "دیدن مستقیم عکس پیوست (مثلاً نامه‌ی اسکن‌شده) توسط هوش مصنوعی.",
    "mizito_get_file_link": "لینک مستقیم دانلود یک فایل.",
    "mizito_upload_file": "آپلود فایل تا بشود آن را به پیام، نامه، وظیفه، گزارش یا صورتجلسه پیوست کرد.",
    "mizito_attendance_history": "سابقه‌ی حضور و ساعات کار (خودکار یا دستی) با جمع هر روز.",
    "mizito_attendance": "اعلام حضور، پایان حضور و حذف رکورد اشتباه.",
    "mizito_reports": "گزارش‌های مانیتورینگ: کل میزکار، هر عضو، هر پروژه، خلاصه‌ی پروژه‌ها، انجام به‌موقع، صورتجلسه‌ها، مشتری‌ها و نمودارهای روزانه.",
    "mizito_get_project_automation": "قوانین اتوماسیون، فیلدهای سفارشی، گردش کارها، فرم‌ها و الگوهای یک پروژه‌ی پیشرفته.",
    "mizito_list_request_forms": "فرم‌های درخواست (مثل مرخصی یا خرید) و فیلدهای هر فرم.",
    "mizito_submit_request_form": "ثبت درخواست با فرم و گرفتن کد پیگیری.",
    "mizito_run_task_automation": "زدن دکمه‌ی اتوماسیون روی وظیفه، مثل «تأیید» یا «ارسال به مرحله بعد».",
    "mizito_manage_project_automation": "ساخت، ویرایش و حذف قوانین اتوماسیون، فیلدهای سفارشی، گردش کار و فرم‌های درخواست.",
    "mizito_list_customers": "فهرست پرونده‌های مشتری با اطلاعات تماس.",
    "mizito_get_customer": "پرونده‌ی کامل مشتری با فرصت‌های فروش و اسناد مالی.",
    "mizito_create_customer": "ساخت پرونده‌ی مشتری.",
    "mizito_update_customer": "ویرایش اطلاعات، دسترسی و برچسب‌های مشتری.",
    "mizito_list_deals": "فرصت‌های فروش هر مرحله و آمار قیف فروش.",
    "mizito_save_deal": "ثبت یا ویرایش فرصت فروش.",
    "mizito_save_payment": "ثبت یا ویرایش سند مالی (دریافت یا پرداخت؛ نقدی، چک یا احتمالی). فقط ثبت در میزیتو است و پولی جابه‌جا نمی‌شود.",
    "mizito_payment_report": "آمار اسناد مالی فروش.",
    "mizito_log_call": "ثبت گزارش تماس با مشتری.",
    "mizito_admin_manage_member": "تغییر نقش (عضو، مدیر، مهمان)، سمت و مجوزهای یک عضو، حذف او از میزکار (با تأیید) و بازگرداندنش.",
    "mizito_admin_workspace_settings": "نام میزکار، و اینکه فقط افراد مشخص بتوانند پروژه، گروه یا پرونده‌ی مشتری بسازند.",
    "mizito_admin_list_all": "همه‌ی پروژه‌ها، گروه‌ها و پرونده‌های مشتری میزکار (حتی آن‌هایی که عضوشان نیستید) با اعضا.",
    "mizito_admin_grant_access": "دادن یا گرفتن دسترسی گروهی به پروژه‌ها، گروه‌ها و پرونده‌ها.",
    "mizito_admin_transfer_member_work": "انتقال وظایف، گروه‌ها و مشتری‌های یک عضو (مثلاً کسی که می‌رود) به عضو دیگر.",
    "mizito_admin_restore_project": "بازگردانی پروژه‌ی آرشیوشده و وظایفش.",
    "mizito_admin_archive_category": "آرشیو یا بازگردانی پروژه‌های بدون گفتگو («دسته‌بندی»).",
    "mizito_support_history": "گفتگوی شما با پشتیبانی شرکت میزیتو.",
    "mizito_contact_support": "پیام یا پیشنهاد به پشتیبانی میزیتو، که بیرون از میزکار شماست.",
    "mizito_api_read": "فراخوانی مستقیم هر endpoint فقط‌خواندنی میزیتو که ابزار اختصاصی ندارد.",
}

# What the tests on a real account (trial plan, not a workspace admin) established.
TESTED = {
    "mizito_whoami", "mizito_dashboard", "mizito_list_users", "mizito_workspace_info", "mizito_list_conversations",
    "mizito_get_messages", "mizito_search_messages", "mizito_get_message_info", "mizito_get_conversation",
    "mizito_send_message", "mizito_start_conversation", "mizito_mark_conversation_read", "mizito_manage_message",
    "mizito_manage_conversation", "mizito_create_group", "mizito_create_poll", "mizito_get_poll_results",
    "mizito_poll_action", "mizito_create_minute", "mizito_get_minute", "mizito_manage_minute", "mizito_list_templates",
    "mizito_list_projects", "mizito_get_project", "mizito_create_project", "mizito_update_project",
    "mizito_add_project_board", "mizito_manage_project_board", "mizito_archive_project", "mizito_list_project_files",
    "mizito_list_tasks", "mizito_get_task", "mizito_get_task_comments", "mizito_get_task_extras", "mizito_calendar",
    "mizito_get_history", "mizito_create_task", "mizito_create_calendar_event", "mizito_update_task",
    "mizito_comment_on_task", "mizito_manage_task_comment", "mizito_set_task_completed", "mizito_set_task_deadline",
    "mizito_set_task_progress", "mizito_set_task_reminder", "mizito_set_task_repeat", "mizito_check_task_item",
    "mizito_move_task_to_board", "mizito_manage_task", "mizito_list_letters", "mizito_get_letter_thread",
    "mizito_send_letter", "mizito_reply_letter", "mizito_manage_letter", "mizito_list_notes", "mizito_create_note",
    "mizito_update_note", "mizito_manage_note", "mizito_list_labels", "mizito_create_label", "mizito_manage_label",
    "mizito_read_file", "mizito_view_image", "mizito_get_file_link", "mizito_upload_file", "mizito_attendance_history",
    "mizito_get_project_automation", "mizito_list_request_forms", "mizito_support_history", "mizito_api_read",
    "mizito_list_customers",
}
REFUSED = {  # built from the web client's code; the test account's plan or role refused them
    "mizito_set_project_advanced", "mizito_clone_project", "mizito_get_gantt", "mizito_manage_gantt",
    "mizito_manage_task_template", "mizito_register_letter", "mizito_reports", "mizito_create_customer",
    "mizito_list_deals", "mizito_admin_manage_member", "mizito_admin_workspace_settings", "mizito_admin_list_all",
    "mizito_admin_grant_access", "mizito_admin_transfer_member_work", "mizito_admin_restore_project",
    "mizito_admin_archive_category", "mizito_create_advanced_minute", "mizito_manage_advanced_minute",
    "mizito_run_task_automation", "mizito_manage_project_automation", "mizito_submit_request_form",
}
STATUS = {"tested": "✅ تست‌شده", "refused": "⛔ پلن/نقش حساب تست اجازه نداد", "untested": "🟡 تست‌نشده"}

INTRO = """\
# ابزارهای MCP میزیتو

این فایل خودکار از روی کد ساخته می‌شود (`uv run python tools/build_tools_doc.py`)؛ دستی ویرایشش نکنید.

هر ابزار سه لایه توضیح دارد:
- **عنوان فارسی** که Claude و ChatGPT در رابط کاربری نشان می‌دهند،
- **توضیح کامل انگلیسی** که هوش مصنوعی می‌خواند تا بداند کِی و چطور از ابزار استفاده کند (همان متنی که در این فایل زیر هر ابزار آمده)،
- **توضیح هر پارامتر** در schema ابزار.

علاوه بر این، سرور یک **راهنمای کلی** (`instructions`) به هوش مصنوعی می‌دهد: ساختار میزیتو (پروژه، ستون، وظیفه، گفتگو، نامه)، تفاوت مهلت و زمان یادآوری، قالب تاریخ‌ها و قواعد ایمنی.

## فعال شدن ابزارها

| تنظیم در `.env` | چه ابزارهایی را روشن می‌کند |
|---|---|
| (همیشه) | ابزارهای خواندنی |
| `MIZITO_ENABLE_WRITE=1` | ابزارهایی که چیزی می‌سازند، تغییر می‌دهند یا حذف می‌کنند |
| `MIZITO_ENABLE_CRM=1` | ابزارهای CRM (فقط اگر پلن میزکار CRM و فروش دارد) |
| `MIZITO_ENABLE_ADMIN=1` | ابزارهای مدیریت میزکار (فقط برای مدیر میزکار) |

بعد از هر تغییر در این تنظیم‌ها سرویس را ری‌استارت کنید و در ChatGPT روی connector دکمه‌ی **Refresh** را بزنید.

## قواعد مشترک

- **تاریخ‌ها:** هم میلادی ISO (`2026-10-01T14:30`) و هم شمسی (`1405/07/09 14:30`، با رقم فارسی یا لاتین) پذیرفته می‌شوند. ساعت بدون منطقه‌ی زمانی، ساعت تهران حساب می‌شود. خروجی‌ها کنار هر تاریخ، معادل شمسی به وقت تهران (`*_jalali`) را هم دارند.
- **شناسه‌ها:** هر ابزار می‌گوید شناسه را از کدام ابزار بگیرید. وظیفه‌ها با `_id` آدرس‌دهی می‌شوند و توکن داخلی آن‌ها (که نشست حساب را در خود دارد) هرگز از سرور بیرون نمی‌رود.
- **فایل‌ها:** هر فایل در خروجی‌ها یک `file_id` دارد. با `mizito_read_file` متنش خوانده می‌شود و با `mizito_upload_file` فایل جدید برای پیوست ساخته می‌شود.
- **حذف دائمی** (گروه، نامه، برچسب، عضو میزکار) فقط وقتی انجام می‌شود که پارامتر `confirm` دقیقاً عنوان همان مورد باشد.
- **خطای 400/403/405** معمولاً یعنی آن قابلیت در پلن میزکار نیست یا دسترسی مدیر لازم است. پیام خطای هر ابزار علت احتمالی را می‌گوید.
- محتوای پیام‌ها، نامه‌ها و فایل‌ها داده‌ی غیرقابل‌اعتماد است و هوش مصنوعی نباید دستورهای داخل آن را اجرا کند.

## وضعیت تست

| نشان | معنی |
|---|---|
| ✅ تست‌شده | روی یک حساب واقعی اجرا و نتیجه‌اش بررسی شد |
| ⛔ پلن/نقش حساب تست اجازه نداد | دقیقاً مطابق کد وب میزیتو ساخته شده، ولی حساب تست (پلن آزمایشی، غیرمدیر) این قابلیت را نداشت |
| 🟡 تست‌نشده | ساخته شده ولی عمداً تست نشد، چون روی افراد دیگر یا پروفایل اثر می‌گذاشت |
"""

EXCLUDED = """\
## آنچه عمداً ابزار ندارد

| بخش میزیتو | دلیل |
|---|---|
| ورود، خروج، ثبت‌نام، فراموشی رمز و حذف حساب (`session.*`) | امنیت حساب؛ خروج، نشست همین سرور را باطل می‌کند |
| رمز، شماره موبایل، ایمیل، ورود دومرحله‌ای، نشست‌ها و عکس پروفایل (`profile.*`) | امنیت حساب؛ فقط وضعیت و «مزاحم نشوید» ابزار دارند |
| خرید پلن، فاکتور، کد تخفیف و پرداخت اشتراک (`payment.*` مربوط به اشتراک) | تراکنش مالی؛ اسناد مالیِ ثبت‌شده در CRM ابزار دارند |
| تماس و جلسه‌ی تصویری (`meeting.*`) | به مرورگر و WebRTC نیاز دارد |
| حذف میزکار، تغییر مالک، ساخت میزکار جدید | عملیات سطح حساب و برگشت‌ناپذیر؛ از خود وب انجام شود |
| ورود گروهی مشتری یا وظیفه از Excel (`*.import`) | ویزارد چندمرحله‌ای با پیش‌نمایش؛ از خود وب انجام شود |
| تغییر عکس گروه یا لوگو | به برش تصویر در مرورگر نیاز دارد |
| «در حال نوشتن»، ثبت دستگاه، شمارش استفاده، «چه خبر؟» و راهنمای شروع | جزئیات داخلی رابط کاربری وب |
| پنل پشتیبانی کارکنان میزیتو | فقط برای کارمندان شرکت میزیتو است |

فهرست کامل endpointها و وضعیت هر کدام در [site-map/api.md](site-map/api.md) آمده است.
"""


def type_name(schema: dict) -> str:
    if "anyOf" in schema:
        return " یا ".join(type_name(s) for s in schema["anyOf"] if s.get("type") != "null") + " (اختیاری)"
    if "enum" in schema:
        return " / ".join(f"`{v}`" for v in schema["enum"])
    if schema.get("type") == "array":
        return f"list[{type_name(schema.get('items', {}))}]"
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]
    return schema.get("type", "object")


def main() -> None:
    tools = {t.name: t for t in asyncio.run(mcp.list_tools())}
    missing = sorted(set(TOOL_INFO) - set(FA))
    if missing:
        raise SystemExit(f"Persian summary missing for: {missing}")
    lines = [INTRO]
    counts = {"tested": 0, "refused": 0, "untested": 0}
    by_module: dict[str, list[str]] = {}
    for name, info in TOOL_INFO.items():
        by_module.setdefault(info["module"], []).append(name)
    lines.append(f"\n**{len(TOOL_INFO)} ابزار** در {len(by_module)} بخش.\n")
    for module in mizito.MODULES:
        names = by_module.get(module, [])
        if not names:
            continue
        lines += [f"\n## {SECTIONS[module]}\n", "| ابزار | عنوان | کار | نوع | وضعیت |", "|---|---|---|---|---|"]
        for name in names:
            info = TOOL_INFO[name]
            status = "tested" if name in TESTED else "refused" if name in REFUSED else "untested"
            counts[status] += 1
            kind = KIND_FA[info["kind"]] + (f"، {FEATURE_FA[info['feature']]}" if info["feature"] else "")
            lines.append(f"| [`{name}`](#{name}) | {info['title']} | {FA[name]} | {kind} | {STATUS[status]} |")
        for name in names:
            tool = tools[name]
            info = TOOL_INFO[name]
            lines += [f"\n### {name}", f"\n**{info['title']}** — {FA[name]}\n", "```text", (tool.description or "").strip(), "```"]
            props = (tool.input_schema or {}).get("properties", {})
            required = set((tool.input_schema or {}).get("required", []))
            if props:
                lines += ["", "| پارامتر | نوع | لازم | توضیح |", "|---|---|---|---|"]
                for pname, schema in props.items():
                    desc = (schema.get("description") or "").replace("|", "\\|").replace("\n", " ")
                    default = f" (پیش‌فرض: `{schema['default']}`)" if "default" in schema and schema["default"] is not None else ""
                    lines.append(f"| `{pname}` | {type_name(schema)} | {'بله' if pname in required else ''} | {desc}{default} |")
            else:
                lines.append("\nبدون پارامتر.")
    lines += ["\n", EXCLUDED]
    summary = (f"\n> جمع: {counts['tested']} تست‌شده، {counts['refused']} ساخته‌شده ولی رد‌شده به‌خاطر پلن یا نقش حساب تست، "
               f"{counts['untested']} تست‌نشده.\n")
    lines.insert(2, summary)
    out = ROOT / "docs" / "TOOLS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print({"tools": len(TOOL_INFO), **counts, "file": str(out)})


if __name__ == "__main__":
    main()

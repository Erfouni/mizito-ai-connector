# Mizito AI Connector

یک MCP Server که حساب [میزیتو](https://mizito.ir) را به **Claude** و **ChatGPT** وصل می‌کند. با آن می‌توانید در چت، گفتگوها، پروژه‌ها، وظایف، نامه‌ها و یادداشت‌ها را بخوانید و تحلیل کنید. اگر بخواهید، ارسال پیام و نامه و ساخت و ویرایش وظیفه هم ممکن است.

*An MCP server that connects a Mizito workspace to Claude and ChatGPT (read, analyse, and optionally act).*

> این پروژه از API داخلی وب‌اپ میزیتو استفاده می‌کند که رسمی نیست. ممکن است با به‌روزرسانی میزیتو تغییر کند. جزئیات API در [API_MAP.md](API_MAP.md) آمده است.

```
Claude.ai / ChatGPT ──HTTPS (MCP)──► سرور شما (این پروژه) ──► app.mizito.ir
```

هر نفر سرور و توکن خودش را دارد. سرور فقط به حساب میزیتوی صاحبش دسترسی دارد.

## پیش‌نیازها

- Python 3.11 یا بالاتر و [uv](https://docs.astral.sh/uv/)
- یک حساب میزیتو
- برای استفاده در **Claude.ai یا ChatGPT** (نسخه‌ی وب و موبایل): یک سرور لینوکسی با دامنه و HTTPS. این سرور باید دو شرط را داشته باشد:
  1. به `app.mizito.ir` دسترسی داشته باشد.
  2. از خارج از ایران در دسترس باشد، چون سرورهای Anthropic و OpenAI از آنجا وصل می‌شوند. این را با [check-host.net](https://check-host.net) تست کنید.

  سرورهای ایرانی معمولاً هر دو شرط را دارند.
- برای connector سفارشی، پلن پولی Claude یا ChatGPT لازم است.

## ۱. نصب و تنظیم ورود

```bash
git clone <آدرس این ریپو> mizito-ai-connector
cd mizito-ai-connector
uv sync
cp .env.example .env
```

در `.env` **یکی** از این دو روش ورود را پر کنید:

- **توکن (تست‌شده):** در تب `office.mizito.ir` دکمه‌ی F12 را بزنید و در Console این را اجرا کنید:
  `copy(localStorage.token)`
  توکن در کلیپ‌بورد کپی می‌شود. آن را جلوی `MIZITO_TOKEN=` بچسبانید. اگر از میزیتو Logout کنید، توکن باطل می‌شود.
- **نام کاربری و رمز (هنوز تست نشده):** `MIZITO_USERNAME` و `MIZITO_PASSWORD` را پر کنید. سرور خودش وارد می‌شود و توکن را تمدید می‌کند. اگر ورود دومرحله‌ای دارید، `MIZITO_LOGIN_CODE` هم لازم است.

تست اتصال:

```bash
uv run python check.py
```

## ۲. استفاده روی کامپیوتر خودتان (Claude Desktop یا Claude Code)

برای Claude Desktop این بخش را به `claude_desktop_config.json` اضافه کنید. در ویندوز این فایل در `%APPDATA%\Claude\` است.

```json
{
  "mcpServers": {
    "mizito": {
      "command": "uv",
      "args": ["--directory", "/path/to/mizito-ai-connector", "run", "server.py"]
    }
  }
}
```

برای Claude Code:

```bash
claude mcp add mizito -- uv --directory /path/to/mizito-ai-connector run server.py
```

## ۳. استقرار روی سرور (برای Claude.ai و ChatGPT)

روی Ubuntu. اول یک رکورد DNS از نوع A برای دامنه‌تان بسازید، مثلاً `mcp.example.com`، که به IP سرور اشاره کند.

```bash
sudo apt install -y python3-venv nginx certbot
sudo useradd --system --home-dir /opt/mizito-mcp --no-create-home --shell /usr/sbin/nologin mizito-mcp

# کد: کپی کنید (scp) یا با دسترسی به ریپو clone کنید
sudo mkdir -p /opt/mizito-mcp && sudo cp server.py mizito_client.py deploy/requirements.txt .env.example /opt/mizito-mcp/
cd /opt/mizito-mcp
sudo python3 -m venv .venv
sudo .venv/bin/pip install --require-hashes -r requirements.txt
```

**تنظیمات سرور.** ابتدا یک مسیر مخفی بسازید:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

بعد `.env.example` را به `.env` کپی کنید (`sudo cp .env.example .env && sudo nano .env`) و این مقدارها را بگذارید:

```
MIZITO_TOKEN=...                 # یا نام کاربری و رمز
MIZITO_ENABLE_WRITE=0            # با 1 ابزارهای نوشتنی روشن می‌شوند
MCP_TRANSPORT=streamable-http
MCP_HOST=127.0.0.1
MCP_PORT=8765
MCP_HTTP_PATH=/mcp-<رشته‌ی مخفی>
MCP_PUBLIC_HOST=mcp.example.com
```

```bash
# ترتیب مهم است: اول کل پوشه، بعد .env که فقط کاربر سرویس بخواند
sudo chown -R root:mizito-mcp /opt/mizito-mcp && sudo chmod -R o-rwx /opt/mizito-mcp
sudo chown mizito-mcp:mizito-mcp .env && sudo chmod 600 .env

# سرویس
sudo cp /path/to/repo/deploy/mizito-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now mizito-mcp

# گواهی HTTPS (nginx برای چند ثانیه متوقف می‌شود)
sudo certbot certonly --standalone -d mcp.example.com \
  --pre-hook "systemctl stop nginx" --post-hook "systemctl start nginx"

# nginx: در فایل، mcp.example.com را با دامنه‌ی خودتان عوض کنید
sudo cp /path/to/repo/deploy/nginx.conf.example /etc/nginx/sites-available/mizito
sudo ln -s /etc/nginx/sites-available/mizito /etc/nginx/sites-enabled/mizito
sudo nginx -t && sudo systemctl reload nginx
```

اگر سرور به Let's Encrypt دسترسی ندارد (بعضی سرورهای ایرانی)، certbot را با `HTTPS_PROXY` اجرا کنید. اگر DNS روی Cloudflare است، از افزونه‌ی `dns-cloudflare` هم می‌توانید استفاده کنید.

آدرس connector شما این است و **مثل رمز** با آن رفتار کنید:

```
https://mcp.example.com/mcp-<رشته‌ی مخفی>
```

## ۴. اضافه کردن به Claude.ai و ChatGPT

- **Claude.ai:** به Settings ← Connectors ← **Add custom connector** بروید، آدرس بالا را وارد کنید و OAuth را خالی بگذارید. در چت، connector را از منوی **+** روشن کنید.
- **ChatGPT:** به Settings ← Apps & Connectors ← Advanced بروید و **Developer mode** را روشن کنید. بعد **Create** را بزنید، آدرس را وارد کنید و Authentication را روی **No authentication** بگذارید. در چت، از منوی **+** گزینه‌ی Developer mode را انتخاب کنید.

ChatGPT فهرست ابزارها را فقط موقع ساخت connector می‌گیرد. هر بار ابزارها عوض شدند (مثلاً بعد از روشن کردن `MIZITO_ENABLE_WRITE`)، روی connector **Refresh** بزنید.

## ابزارها

**خواندن** (همیشه فعال):

| ابزار | کار |
|---|---|
| `mizito_whoami` / `mizito_switch_workspace` | کاربر فعلی و میزکارها، و جابه‌جایی بین میزکارها |
| `mizito_dashboard` | شمارنده‌ها: نامه‌ها و پیام‌های خوانده‌نشده، کارهای امروز و عقب‌افتاده |
| `mizito_list_users` | اعضای میزکار |
| `mizito_list_conversations` / `mizito_get_messages` / `mizito_search_messages` | گفتگوها، پیام‌ها (تا ۶۰۰ پیام در هر فراخوانی) و جستجو |
| `mizito_list_projects` / `mizito_get_project` | پروژه‌ها |
| `mizito_list_tasks` / `mizito_get_task` / `mizito_get_task_comments` | وظایف: کارهای من، پیگیری از دیگران، وظایف یک پروژه، انجام‌شده‌ها |
| `mizito_list_letters` / `mizito_get_letter_thread` | کارتابل نامه‌ها |
| `mizito_list_notes` | یادداشت‌ها |
| `mizito_api_read` | فراخوانی هر endpoint فقط‌خواندنی دیگر |

خواندن پیام‌ها آن‌ها را «دیده‌شده» علامت نمی‌زند.

**نوشتن** (فقط با `MIZITO_ENABLE_WRITE=1`):

| ابزار | کار |
|---|---|
| `mizito_send_message` / `mizito_start_conversation` / `mizito_mark_conversation_read` | ارسال پیام (با امکان پاسخ به یک پیام)، شروع گفتگوی خصوصی، علامت خوانده‌شده |
| `mizito_create_task` / `mizito_update_task` / `mizito_comment_on_task` | ساخت وظیفه **داخل یک پروژه** (در میزیتو اجباری است)، ویرایش، کامنت |
| `mizito_set_task_completed` / `mizito_set_task_deadline` / `mizito_set_task_progress` / `mizito_check_task_item` | تکمیل یا بازکردن دوباره، مهلت، درصد پیشرفت، تیک چک‌لیست |
| `mizito_send_letter` / `mizito_reply_letter` | ارسال نامه و پاسخ داخل یک رشته |
| `mizito_create_note` / `mizito_create_project` | ساخت یادداشت و پروژه |

این ابزارها روی یک حساب واقعی تست شده‌اند. فقط ساختن گفتگوی خصوصیِ **تازه** و تغییر مسئولان وظیفه هنوز تست نشده‌اند.
حذف کردن هر چیزی و مدیریت میزکار و حساب (عضوها، نقش‌ها، رمز، پرداخت) عمداً پشتیبانی نمی‌شوند.

## امنیت

- **آدرس connector:** مسیر مخفی داخلش تنها چیزی است که جلوی دسترسی دیگران را می‌گیرد. آن را به کسی ندهید. اگر لو رفت، `MCP_HTTP_PATH` را عوض کنید.
- **فایل `.env`:** یعنی دسترسی کامل به حساب میزیتو. هرگز commit نشود (در `.gitignore` هست).
- **ابزارهای نوشتنی:** ChatGPT و Claude قبل از هر عمل نوشتنی از کاربر تأیید می‌گیرند. با این حال متن پیام‌ها را داده‌ی غیرقابل‌اعتماد بدانید و فقط وقتی لازم است نوشتن را روشن کنید.
- **توکن وظیفه‌ها:** `access_token` وظیفه‌ها در میزیتو توکن نشست حساب را بدون رمزگذاری داخل خودش دارد. این سرور وظیفه‌ها را فقط با `_id` آدرس‌دهی می‌کند و هر JWT را از خروجی‌ها حذف می‌کند.
- **لاگ‌ها:** سرور access log ندارد و nginx هم برای این سایت لاگ دسترسی ثبت نمی‌کند، تا مسیر مخفی جایی ثبت نشود.
- **حریم خصوصی:** محتوای میزیتو به Anthropic یا OpenAI فرستاده می‌شود. این را با سیاست سازمان‌تان هماهنگ کنید.

## عیب‌یابی

| مشکل | علت و راه‌حل |
|---|---|
| `No credentials` | `MIZITO_TOKEN` در `.env` خالی است |
| `401` / `token expired` | توکن باطل شده است. توکن تازه بگذارید و سرویس را ری‌استارت کنید |
| ChatGPT ابزار جدید را نمی‌بیند | روی connector **Refresh** بزنید و یک چت جدید باز کنید |
| ساخت وظیفه رد می‌شود | `project_id` لازم است، و مسئولان باید عضو همان پروژه باشند |
| اسمی پیدا نمی‌شود | بعضی اسم‌ها با «ي» و «ك» عربی نوشته شده‌اند |
| `monitor.*` خطای 400 می‌دهد | پارامتر یا دسترسی مدیر لازم دارد |

## فایل‌ها

| فایل | کار |
|---|---|
| `server.py` | ابزارهای MCP و اجرای stdio یا HTTP |
| `mizito_client.py` | کلاینت API میزیتو (ورود، فراخوانی، حذف اسرار از خروجی) |
| `check.py` | تست کامل اتصال و ابزارهای خواندنی |
| `deploy/` | سرویس systemd، نمونه‌ی nginx و `requirements.txt` با hash |
| `API_MAP.md` | نقشه‌ی API داخلی میزیتو |

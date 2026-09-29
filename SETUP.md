# راهنمای راه‌اندازی · Setup guide

[فارسی](#فارسی) · [English](#english)

---

<div dir="rtl">

## فارسی

با این راهنما حساب میزیتوی خودتان را به **ChatGPT** و **Claude** وصل می‌کنید. فقط دو چیز لازم است: **یک دامنه** و **حساب میزیتوی خودتان**. بقیه‌ی کارها را اسکریپت نصب خودش انجام می‌دهد.

### پیش از شروع

- **یک سرور لینوکسی** با Ubuntu 24.04 (یا 22.04، یا Debian 12) و دسترسی root. این سرور دو شرط دارد:
  - سایت میزیتو را باز کند. سرورهای داخل ایران معمولاً این شرط را دارند.
  - از خارج ایران در دسترس باشد، چون ChatGPT و Claude از آنجا وصل می‌شوند. با [check-host.net](https://check-host.net) امتحانش کنید.
- **یک دامنه یا زیردامنه**، مثلاً `mcp.example.com`، با رکورد **A** که به IP سرور اشاره کند. اگر دامنه روی Cloudflare است، ابر نارنجی را خاموش کنید (DNS only).
- **حساب پولی ChatGPT یا Claude**. ChatGPT برای Developer mode لازمش دارد، Claude برای custom connector.

### گام ۱: گرفتن توکن میزیتو

1. در مرورگر کامپیوتر وارد `office.mizito.ir` شوید.
2. کلید **F12** را بزنید و به تب **Console** بروید.
3. این را تایپ کنید و Enter بزنید: `copy(localStorage.token)`.
   اگر Chrome اجازه‌ی Paste نداد، اول `allow pasting` را تایپ کنید و Enter بزنید.
4. توکن در کلیپ‌بورد کپی شد. آن را مثل رمز عبور نگه دارید.

> اگر در مرورگر از میزیتو خارج شوید (Logout)، توکن باطل می‌شود. به‌جای توکن می‌توانید نام کاربری و رمز هم بدهید.

### گام ۲: نصب روی سرور (یک دستور)

با SSH وارد سرور شوید و این سه خط را اجرا کنید:

```bash
git clone https://github.com/Erfouni/mizito-ai-connector.git
cd mizito-ai-connector
sudo bash deploy/install.sh
```

اسکریپت فقط **دو سؤال** می‌پرسد:

1. **دامنه**، مثلاً `mcp.example.com`.
2. **توکن میزیتو**. اگر فقط Enter بزنید، نام کاربری و رمز را می‌پرسد.

بقیه‌ی کارها خودکار است: نصب پایتون و بسته‌ها، ساخت سرویسی که همیشه روشن می‌ماند، گرفتن گواهی HTTPS رایگان، تنظیم nginx و ساختن آدرس مخفی. در پایان **آدرس connector** شما نمایش داده می‌شود.

### گام ۳: وصل کردن به ChatGPT یا Claude

- **ChatGPT:**
  1. Settings ← Apps & Connectors ← Advanced را باز کنید و **Developer mode** را روشن کنید.
  2. **Create** را بزنید، آدرس را بچسبانید و Authentication را روی **No authentication** بگذارید.
  3. در چت، از منوی **+** گزینه‌ی Developer mode و connector میزیتو را انتخاب کنید.
- **Claude.ai:**
  1. Settings ← Connectors ← **Add custom connector** را باز کنید و آدرس را بچسبانید. بخش OAuth را خالی بگذارید.
  2. در چت، connector را از منوی **+** روشن کنید.

حالا امتحان کنید، مثلاً: «کارهای امروزم در میزیتو چیست؟»

### کارهای بعدی

| کار | دستور (روی سرور، داخل پوشه‌ی `mizito-ai-connector`) |
|---|---|
| دیدن دوباره‌ی آدرس connector | `sudo bash deploy/install.sh url` |
| به‌روزرسانی به نسخه‌ی جدید | `git pull && sudo bash deploy/install.sh`، بعد در ChatGPT روی connector دکمه‌ی **Refresh** را بزنید |
| عوض کردن توکن | `sudo nano /opt/mizito-mcp/.env`، مقدار `MIZITO_TOKEN` را عوض کنید، بعد `sudo systemctl restart mizito-mcp` |
| فقط خواندن (بدون ارسال یا تغییر) | در همان فایل بگذارید `MIZITO_ENABLE_WRITE=0` و سرویس را ری‌استارت کنید |
| ابزارهای CRM یا مدیریت میزکار | `MIZITO_ENABLE_CRM=1` یا `MIZITO_ENABLE_ADMIN=1`، فقط اگر پلن و نقش شما اجازه می‌دهد؛ بعد سرویس را ری‌استارت کنید |
| دیدن لاگ سرویس | `sudo journalctl -u mizito-mcp -f` |

### مشکلات رایج

| پیام | راه‌حل |
|---|---|
| `cannot reach app.mizito.ir` | سرور به میزیتو دسترسی ندارد. از سروری استفاده کنید که میزیتو را باز می‌کند، مثلاً سروری در ایران. |
| `does not resolve` | رکورد A دامنه را بسازید، چند دقیقه صبر کنید و اسکریپت را دوباره اجرا کنید. |
| `No certificate` | پورت 80 باید از اینترنت باز باشد. اگر سرور به Let's Encrypt دسترسی ندارد (بعضی سرورهای ایرانی)، اسکریپت را با پراکسی اجرا کنید: `sudo HTTPS_PROXY=http://host:port bash deploy/install.sh` |
| `Installing Python packages failed` | اگر pypi.org روی سرور بسته است، از یک mirror استفاده کنید: `sudo PIP_INDEX_URL=https://<mirror>/simple bash deploy/install.sh` |
| `Mizito refused the login` | توکن باطل شده است. توکن تازه بگذارید (جدول بالا). |
| ChatGPT ابزارها را نمی‌بیند | روی connector دکمه‌ی **Refresh** را بزنید و یک چت جدید باز کنید. |

### امنیت

- آدرس connector مثل **رمز عبور** است و آن را به کسی ندهید. هر کس آن را داشته باشد به میزیتوی شما دسترسی دارد.
- ChatGPT و Claude قبل از هر ارسال یا تغییری از شما تأیید می‌گیرند.
- محتوای میزیتو برای پردازش به OpenAI یا Anthropic فرستاده می‌شود. این را با سیاست سازمان‌تان هماهنگ کنید.

### بدون سرور، فقط روی کامپیوتر خودتان (Claude Desktop)

اگر فقط Claude Desktop روی کامپیوتر خودتان کافی است، سرور و دامنه لازم ندارید:

1. [uv](https://docs.astral.sh/uv/getting-started/installation/) را نصب کنید. بعد ریپو را دانلود کنید و این‌ها را اجرا کنید: `cd mizito-ai-connector`، `uv sync` و کپی کردن `.env.example` به `.env`.
2. در فایل `.env` توکن را جلوی `MIZITO_TOKEN=` بچسبانید و بگذارید `MIZITO_ENABLE_WRITE=1`.
3. با `uv run python check.py` اتصال را تست کنید.
4. در Claude Desktop به Settings ← Developer ← Edit Config بروید، بخش زیر را اضافه کنید (مسیر را با مسیر خودتان عوض کنید) و Claude را دوباره باز کنید.

</div>

```json
{
  "mcpServers": {
    "mizito": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\mizito-ai-connector", "run", "server.py"]
    }
  }
}
```

---

## English

This guide connects your own Mizito account to **ChatGPT** and **Claude**. You only need **a domain** and **your Mizito account**. The install script does everything else.

### Before you start

- **A Linux server**: Ubuntu 24.04 (or 22.04, or Debian 12), with root access. It must meet two conditions:
  - It can open Mizito. Servers inside Iran usually can.
  - It is reachable from outside Iran, because ChatGPT and Claude connect from there. Test this with [check-host.net](https://check-host.net).
- **A domain or subdomain**, e.g. `mcp.example.com`, with an **A record** pointing to the server's IP. On Cloudflare, turn the orange cloud off (DNS only).
- **A paid ChatGPT or Claude plan**. ChatGPT needs it for Developer mode, Claude for custom connectors.

### Step 1: get your Mizito token

1. Log in to `office.mizito.ir` in a desktop browser.
2. Press **F12** and open the **Console** tab.
3. Type `copy(localStorage.token)` and press Enter. If Chrome blocks pasting, type `allow pasting` first.
4. The token is now in your clipboard. Treat it like a password.

> Logging out of Mizito in that browser invalidates the token. You can also use your username and password instead.

### Step 2: install on the server (one command)

Connect to the server with SSH and run:

```bash
git clone https://github.com/Erfouni/mizito-ai-connector.git
cd mizito-ai-connector
sudo bash deploy/install.sh
```

The script asks **two questions**:

1. **Your domain**, e.g. `mcp.example.com`.
2. **Your Mizito token**. If you just press Enter, it asks for your username and password instead.

Everything else is automatic:
- Python and its packages.
- A background service that stays running.
- A free HTTPS certificate.
- nginx.
- A secret connector address.

At the end the script prints **your connector address**.

### Step 3: connect ChatGPT or Claude

- **ChatGPT:**
  1. Open Settings → Apps & Connectors → Advanced, and turn on **Developer mode**.
  2. Click **Create**, paste the address, and set Authentication to **No authentication**.
  3. In a chat, pick Developer mode and the Mizito connector from the **+** menu.
- **Claude.ai:**
  1. Open Settings → Connectors → **Add custom connector** and paste the address. Leave OAuth empty.
  2. In a chat, turn the connector on from the **+** menu.

Then try it: "What are my Mizito tasks for today?"

### Later

| Task | Command (on the server, inside `mizito-ai-connector`) |
|---|---|
| Show the connector address again | `sudo bash deploy/install.sh url` |
| Update to a new version | `git pull && sudo bash deploy/install.sh`, then click **Refresh** on the connector in ChatGPT |
| Change the token | `sudo nano /opt/mizito-mcp/.env`, replace `MIZITO_TOKEN`, then `sudo systemctl restart mizito-mcp` |
| Read-only mode (no sending or changes) | Set `MIZITO_ENABLE_WRITE=0` in that file and restart |
| CRM or workspace-admin tools | Set `MIZITO_ENABLE_CRM=1` or `MIZITO_ENABLE_ADMIN=1` if your plan and role allow it, then restart |
| Service log | `sudo journalctl -u mizito-mcp -f` |

### Troubleshooting

| Message | Fix |
|---|---|
| `cannot reach app.mizito.ir` | The server cannot open Mizito. Use a server that can, e.g. one in Iran. |
| `does not resolve` | Create the A record for your domain, wait a few minutes and run the script again. |
| `No certificate` | Port 80 must be open to the internet. If the server cannot reach Let's Encrypt (some Iranian servers), use a proxy: `sudo HTTPS_PROXY=http://host:port bash deploy/install.sh` |
| `Installing Python packages failed` | If pypi.org is blocked, use a mirror: `sudo PIP_INDEX_URL=https://<mirror>/simple bash deploy/install.sh` |
| `Mizito refused the login` | The token has expired. Put in a fresh one (see the table above). |
| ChatGPT does not see the tools | Click **Refresh** on the connector and start a new chat. |

### Security

- The connector address works like a **password**: keep it private. Anyone who has it can use your Mizito account.
- ChatGPT and Claude ask you before anything is sent or changed.
- Mizito content is sent to OpenAI or Anthropic for processing. Check that this fits your organisation's policy.

### Without a server: only on your own computer (Claude Desktop)

For Claude Desktop on your own computer you need no server and no domain:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and download the repository.
2. Run `cd mizito-ai-connector` and `uv sync`, then copy `.env.example` to `.env`.
3. In `.env`, paste the token after `MIZITO_TOKEN=` and set `MIZITO_ENABLE_WRITE=1`.
4. Test with `uv run python check.py`.
5. In Claude Desktop open Settings → Developer → Edit Config and add the JSON block from the Persian section above, with your own path. Then restart Claude.

All tools are described in [docs/TOOLS.md](docs/TOOLS.md). Technical details are in [README.md](README.md).

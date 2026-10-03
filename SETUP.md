# راهنمای راه‌اندازی · Setup guide

[فارسی](#فارسی) · [English](#english)

---

<div dir="rtl">

## فارسی

با این راهنما حساب میزیتوی خودتان را به **ChatGPT** یا **Claude** وصل می‌کنید. سه قدم دارد و حدود ده دقیقه طول می‌کشد.

**لازم دارید:**

- **یک سرور Ubuntu** (۲۲.۰۴ یا ۲۴.۰۴) که میزیتو را باز کند و از خارج ایران هم در دسترس باشد. بیشتر سرورهای ایرانی این‌طورند.
- **یک دامنه یا زیردامنه**، مثلاً `mcp.example.com`.
- **نام کاربری و رمز میزیتو**.
- **پلن پولی ChatGPT یا Claude**.

### قدم ۱: دامنه را به سرور وصل کنید

در پنل دامنه (یا Cloudflare) یک رکورد بسازید:

| نوع (Type) | نام (Name) | مقدار (Value) |
|---|---|---|
| `A` | `mcp` یا هر اسم دیگر | IP سرور |

اگر دامنه روی Cloudflare است، **ابر نارنجی را خاموش کنید** تا خاکستری شود (DNS only).

### قدم ۲: نصب با یک دستور

با SSH وارد سرور شوید، این خط را کپی کنید و Enter بزنید:

```bash
curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | bash
```

فقط سه سؤال می‌پرسد:

1. **دامنه**، مثلاً `mcp.example.com`.
2. **نام کاربری میزیتو**: شماره‌ی موبایل یا ایمیل.
3. **رمز میزیتو**. موقع تایپ دیده نمی‌شود.

اگر ورود دومرحله‌ای دارید، کد پیامکی را هم می‌پرسد. رمز اشتباه باشد، دوباره می‌پرسد. بقیه‌ی کارها خودکار است و در آخر **آدرس connector** نمایش داده می‌شود. آن را کپی کنید.

### قدم ۳: آدرس را در ChatGPT یا Claude بگذارید

- **Claude:** Settings ← Connectors ← **Add custom connector** ← آدرس را بچسبانید. بخش OAuth را خالی بگذارید.
- **ChatGPT:** Settings ← Apps & Connectors ← Advanced ← **Developer mode** را روشن کنید ← **Create** ← آدرس را بچسبانید ← Authentication: **No authentication**.

در چت، connector میزیتو را از منوی **+** روشن کنید و بپرسید: «کارهای امروزم در میزیتو چیست؟»

### بعداً

این دستورها را روی سرور، در هر پوشه‌ای، می‌توانید بزنید:

| دستور | کار |
|---|---|
| `mizito-connector url` | آدرس connector را دوباره نشان می‌دهد |
| `mizito-connector status` | بررسی می‌کند همه‌چیز کار می‌کند یا نه |
| `mizito-connector login` | دوباره وارد میزیتو می‌شود (مثلاً وقتی رمز را عوض کرده‌اید) |
| `mizito-connector update` | به آخرین نسخه به‌روز می‌کند. بعدش در ChatGPT روی connector دکمه‌ی **Refresh** را بزنید |
| `mizito-connector logs` | لاگ سرویس را نشان می‌دهد |

### اگر خطا داد

خود اسکریپت می‌گوید مشکل چیست و چه باید کرد. مشکل را برطرف کنید و **همان دستور نصب را دوباره بزنید**. تنظیمات قبلی حفظ می‌شوند و نصب از همان‌جا ادامه پیدا می‌کند.

| پیام | راه‌حل |
|---|---|
| `has no DNS record yet` | قدم ۱ را انجام دهید، چند دقیقه صبر کنید و دوباره بزنید. |
| `points to Cloudflare's proxy` | ابر نارنجی Cloudflare را خاموش کنید و دوباره بزنید. |
| `cannot reach app.mizito.ir` | این سرور میزیتو را باز نمی‌کند. از سرور دیگری استفاده کنید، مثلاً سروری در ایران. |
| `Let's Encrypt could not check` | پورت 80 باید از اینترنت باز باشد. فایروال پنل سرور را هم بررسی کنید. |
| `cannot reach Let's Encrypt` | سرور به خارج دسترسی ندارد. اگر پراکسی دارید: `sudo HTTPS_PROXY=http://IP:PORT mizito-connector update` |
| `Port 80 is already used` | برنامه‌ی دیگری روی پورت 80 یا 443 است. آن را متوقف کنید، چون این نصب nginx لازم دارد. |
| ChatGPT ابزارها را نمی‌بیند | روی connector دکمه‌ی **Refresh** را بزنید و یک چت تازه باز کنید. |

### امنیت

- آدرس connector مثل **رمز عبور** است و آن را به کسی ندهید.
- رمز میزیتو فقط روی سرور خودتان ذخیره می‌شود، در فایل `/opt/mizito-mcp/.env` که فقط سرویس می‌تواند بخواندش. با آن، سرور هر وقت لازم شد خودش دوباره وارد میزیتو می‌شود.
- ChatGPT و Claude قبل از هر ارسال یا تغییری از شما تأیید می‌گیرند.
- محتوای میزیتو برای پردازش به OpenAI یا Anthropic فرستاده می‌شود. این را با سیاست سازمان‌تان هماهنگ کنید.

<details>
<summary><b>تنظیمات بیشتر</b> (اختیاری)</summary>

- **توکن به‌جای رمز:** وقتی نام کاربری را پرسید، فقط Enter بزنید تا توکن را بپرسد. توکن را این‌طور می‌گیرید: در مرورگر وارد `office.mizito.ir` شوید، F12 را بزنید و در تب Console این را بنویسید: `copy(localStorage.token)`. توکن با خروج از میزیتو (Logout) باطل می‌شود. رمز ماندگارتر است.
- **فقط خواندن** (بدون ارسال یا تغییر): در `/opt/mizito-mcp/.env` بگذارید `MIZITO_ENABLE_WRITE=0` و بعد `sudo systemctl restart mizito-mcp` را بزنید.
- **ابزارهای CRM یا مدیریت میزکار:** در همان فایل `MIZITO_ENABLE_CRM=1` یا `MIZITO_ENABLE_ADMIN=1` بگذارید، اگر پلن و نقش شما اجازه می‌دهد.
- **بسته‌های پایتون:** اگر pypi.org روی سرور باز نباشد، اسکریپت خودش از mirrorهای ایرانی استفاده می‌کند. برای یک mirror دیگر: `sudo PIP_INDEX_URL=https://<mirror>/simple mizito-connector update`.
- **وب‌سرور خودتان** (بدون nginx و HTTPS این اسکریپت): `curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | MIZITO_SKIP_TLS=1 bash`. بعد وب‌سرورتان را به `127.0.0.1:8765` وصل کنید.
- **نصب از نسخه‌ی دانلودشده‌ی ریپو:** داخل پوشه‌ی ریپو بزنید `sudo bash install.sh`.

</details>

</div>

<details>
<summary dir="rtl"><b>بدون سرور، فقط روی کامپیوتر خودتان</b> (Claude Desktop)</summary>

<div dir="rtl">

اگر فقط Claude Desktop روی کامپیوتر خودتان کافی است، سرور و دامنه لازم ندارید:

1. [uv](https://docs.astral.sh/uv/getting-started/installation/) را نصب کنید و ریپو را دانلود کنید.
2. داخل پوشه‌ی ریپو بزنید `uv sync` و `.env.example` را به `.env` کپی کنید.
3. در `.env` نام کاربری و رمز (`MIZITO_USERNAME` و `MIZITO_PASSWORD`) یا توکن (`MIZITO_TOKEN`) را بگذارید، و `MIZITO_ENABLE_WRITE=1`.
4. با `uv run python check.py` اتصال را امتحان کنید.
5. در Claude Desktop به Settings ← Developer ← Edit Config بروید، بخش زیر را اضافه کنید (مسیر را با مسیر خودتان عوض کنید) و Claude را دوباره باز کنید.

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

</details>

---

## English

This guide connects your own Mizito account to **ChatGPT** or **Claude**. It takes three steps and about ten minutes.

**You need:**

- **An Ubuntu server** (22.04 or 24.04) that can open Mizito and is reachable from outside Iran. Most Iranian servers are.
- **A domain or subdomain**, e.g. `mcp.example.com`.
- **Your Mizito username and password**.
- **A paid ChatGPT or Claude plan**.

### Step 1: point the domain to the server

At your domain provider (or Cloudflare), add this record:

| Type | Name | Value |
|---|---|---|
| `A` | `mcp`, or any other name | the server's IP |

On Cloudflare, **turn the orange cloud off** so it is grey (DNS only).

### Step 2: install with one command

Connect to the server with SSH, paste this line and press Enter:

```bash
curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | bash
```

It asks only three questions:

1. **Your domain**, e.g. `mcp.example.com`.
2. **Your Mizito username**: mobile number or email.
3. **Your Mizito password**. It is hidden while you type.

With two-step login it also asks for the SMS code. If the password is wrong, it asks again. Everything else is automatic, and at the end it shows **your connector address**. Copy it.

### Step 3: add the address in ChatGPT or Claude

- **Claude:** Settings → Connectors → **Add custom connector** → paste the address. Leave OAuth empty.
- **ChatGPT:** Settings → Apps & Connectors → Advanced → turn on **Developer mode** → **Create** → paste the address → Authentication: **No authentication**.

In a chat, turn on the Mizito connector from the **+** menu and ask: "What are my Mizito tasks for today?"

### Later

Run these on the server, from any folder:

| Command | What it does |
|---|---|
| `mizito-connector url` | Shows the connector address again |
| `mizito-connector status` | Checks that everything works |
| `mizito-connector login` | Logs in to Mizito again, e.g. after you change your password |
| `mizito-connector update` | Updates to the latest version. Then click **Refresh** on the connector in ChatGPT |
| `mizito-connector logs` | Shows the service log |

### If something goes wrong

The script says what is wrong and what to do. Fix it and **run the same install command again**. Your settings are kept and the installation continues from there.

| Message | Fix |
|---|---|
| `has no DNS record yet` | Do step 1, wait a few minutes, then run it again. |
| `points to Cloudflare's proxy` | Turn Cloudflare's orange cloud off, then run it again. |
| `cannot reach app.mizito.ir` | This server cannot open Mizito. Use another server, e.g. one in Iran. |
| `Let's Encrypt could not check` | Port 80 must be open to the internet. Also check the firewall in your server provider's panel. |
| `cannot reach Let's Encrypt` | The server has no access abroad. With a proxy: `sudo HTTPS_PROXY=http://IP:PORT mizito-connector update` |
| `Port 80 is already used` | Another program uses port 80 or 443. Stop it, because this installer needs nginx. |
| ChatGPT does not see the tools | Click **Refresh** on the connector and start a new chat. |

### Security

- The connector address works like a **password**: keep it private.
- Your Mizito password is stored only on your own server, in `/opt/mizito-mcp/.env`, which only the service can read. With it the server logs in again by itself whenever needed.
- ChatGPT and Claude ask you before anything is sent or changed.
- Mizito content is sent to OpenAI or Anthropic for processing. Check that this fits your organisation's policy.

<details>
<summary><b>More options</b> (optional)</summary>

- **A token instead of the password:** when it asks for the username, just press Enter and it asks for a token. To get one, log in to `office.mizito.ir` in a browser, press F12 and type `copy(localStorage.token)` in the Console tab. A token stops working when you log out of Mizito; the password lasts longer.
- **Read-only** (no sending or changes): set `MIZITO_ENABLE_WRITE=0` in `/opt/mizito-mcp/.env`, then run `sudo systemctl restart mizito-mcp`.
- **CRM or workspace-admin tools:** set `MIZITO_ENABLE_CRM=1` or `MIZITO_ENABLE_ADMIN=1` in that file, if your plan and role allow it.
- **Python packages:** if pypi.org is blocked on the server, the script uses Iranian mirrors by itself. For another mirror: `sudo PIP_INDEX_URL=https://<mirror>/simple mizito-connector update`.
- **Your own web server** (no nginx or HTTPS from this script): `curl -fsSL https://raw.githubusercontent.com/Erfouni/mizito-ai-connector/main/install.sh | MIZITO_SKIP_TLS=1 bash`, then point your web server to `127.0.0.1:8765`.
- **From a downloaded copy of the repository:** run `sudo bash install.sh` inside it.

</details>

<details>
<summary><b>Without a server: only on your own computer</b> (Claude Desktop)</summary>

For Claude Desktop on your own computer you need no server and no domain:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and download the repository.
2. Inside it, run `uv sync` and copy `.env.example` to `.env`.
3. In `.env`, put your username and password (`MIZITO_USERNAME`, `MIZITO_PASSWORD`) or a token (`MIZITO_TOKEN`), and set `MIZITO_ENABLE_WRITE=1`.
4. Test with `uv run python check.py`.
5. In Claude Desktop open Settings → Developer → Edit Config, add this (with your own path) and restart Claude:

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

</details>

All tools are described in [docs/TOOLS.md](docs/TOOLS.md). Technical details are in [README.md](README.md).

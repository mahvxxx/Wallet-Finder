# 🔍 Wallet Founder by Mahvxxx™  
# Version: 2.7  

**Wallet Founder** is an automated script for generating and checking Bitcoin wallets. This tool randomly creates Bitcoin addresses and checks their balance. It also uses a Telegram bot to send status reports and alerts.  

**Wallet Founder** یک اسکریپت خودکار برای تولید و بررسی کیف پول‌های بیتکوین است. این ابزار آدرس‌های بیتکوین را به‌صورت تصادفی ایجاد کرده و موجودی آن‌ها را بررسی می‌کند. همچنین با استفاده از یک ربات تلگرامی، گزارش‌های وضعیت و هشدارها را برای شما ارسال می‌کند.  

---
## ✨ Features | ویژگی‌ها  

✅ **Automatic Bitcoin Wallet Checking** – Generates and verifies an unlimited number of Bitcoin addresses automatically.  
✅ **Telegram Integration** – Sends status reports and alerts via a Telegram bot and tests the script status.  
✅ **Logging System** – Saves information about checked wallets, errors, and wallets with a balance.  
✅ **Smart Reporting System** – Sends a complete report every 6 hours, including the number of checks, errors, and valid wallets.  
✅ **Issue Detection** – If no wallet is checked for more than 1 hour, an alert is sent.  
✅ **Easy Installation** – Installs all dependencies and sets up the project with a single command.  
✅ **Cross-Platform Compatibility** – Runs on Windows, Linux, and macOS.  

✅ **بررسی خودکار کیف پول‌های بیتکوین** – تولید و بررسی بی‌نهایت آدرس بیتکوین به‌صورت خودکار.  
✅ **اتصال به تلگرام** – ارسال گزارش‌های وضعیت و هشدارها از طریق ربات تلگرامی و تست وضعیت اسکریپت.  
✅ **ثبت لاگ‌های بررسی و خطاها** – ذخیره اطلاعات کیف پول‌های بررسی‌شده، خطاها و ولت‌های دارای موجودی.  
✅ **سیستم گزارش‌دهی هوشمند** – ارسال گزارش کامل از تعداد بررسی‌ها، خطاها و کیف پول‌های معتبر هر ۶ ساعت.  
✅ **شناسایی مشکلات در اجرا** – در صورتی که بیش از ۱ ساعت هیچ کیف پولی بررسی نشود، هشدار ارسال می‌شود.  
✅ **نصب آسان** – تنها با اجرای یک دستور، تمام وابستگی‌ها نصب شده و پروژه آماده اجرا می‌شود.  
✅ **سازگاری با تمام سیستم‌عامل‌ها** – قابل اجرا در ویندوز، لینوکس و مک.  

---
## 📥 Installation | نصب  

### 🔹 On Linux & macOS | روی لینوکس و مک  
To download the repository, run the following command in your terminal:  
برای دانلود ریپازیتوری، دستور زیر را در ترمینال خود وارد کنید:  

```bash
curl -sSL https://raw.githubusercontent.com/mahvxxx/wallet-founder/main/setup.sh | bash
```

The **wallet-founder** folder will be downloaded in your directory.  
پوشه **wallet-founder** در دایرکتوری شما دانلود خواهد شد.  

### 🔹 On Windows | روی ویندوز  
To download the repository, follow these steps:  
برای دانلود ریپازیتوری، اقدامات زیر را انجام دهید:  

1. Open **Command Prompt (CMD)**.  
   ابتدا یک **Command Prompt (CMD)** باز کنید.  
2. Run the following command:  
   سپس دستور زیر را وارد کنید:  

   ```batch
   powershell -Command "Invoke-WebRequest -Uri 'https://github.com/mahvxxx/wallet-founder/raw/main/setup.bat' -OutFile 'setup.bat'; Start-Process 'setup.bat'"
   ```

---
## ▶️ Running the Script | اجرای اسکریپت  

### 🔹 On Linux & macOS | روی لینوکس و مک  
Open the terminal and run the following commands:  
ترمینال را باز کنید و دستورات زیر را وارد کنید:  

```bash
cd wallet-founder
python3 wallet-founder.py
```

### 🔹 On Windows | روی ویندوز  
Open the terminal and run the following commands:  
ترمینال را باز کنید و دستورات زیر را وارد کنید:  

```cmd
cd wallet-founder
python wallet-founder.py
```

---
## 🤖 Telegram Bot Setup | تنظیم ربات تلگرام  

### 📌 Entering Information in the Program | ورود اطلاعات در برنامه  
After running the program, you will be prompted to enter the following information:  
پس از اجرای برنامه، از شما خواسته می‌شود که اطلاعات زیر را وارد کنید:  

1. **Device Name** – Must be unique and not repeated.  
   **نام دستگاه** – این مقدار باید یکتا باشد و تکراری نباشد.  
2. **Device ID** – Must also be unique.  
   **شماره دستگاه** – این مقدار نیز باید یکتا باشد.  
3. **Bot Token** – Obtained from BotFather.  
   **توکن ربات** – که از BotFather دریافت خواهید کرد.  
4. **Chat ID** – Obtained from userinfobot.  
   **چت آیدی** – که از userinfobot دریافت خواهید کرد.  

The program automatically saves the information in the `TelegramBot-config.txt` file.  
برنامه به‌صورت خودکار اطلاعات را ذخیره کرده و در فایل `TelegramBot-config.txt` قرار می‌دهد.  

---
### 🔹 Getting the Bot Token | دریافت توکن ربات  
If you don’t have a Telegram bot yet, follow these steps:  
اگر هنوز ربات تلگرام ندارید، مراحل زیر را دنبال کنید:  

1. Message **[@BotFather](https://t.me/BotFather)** on Telegram.  
   به **[@BotFather](https://t.me/BotFather)** در تلگرام پیام دهید.  
2. Send the command `/newbot` and choose a name for your bot.  
   دستور `/newbot` را ارسال کنید و یک نام برای ربات خود انتخاب کنید.  
3. Copy the provided token (something like `123456789:ABCDEF...`).  
   توکن ارائه‌شده را کپی کنید (چیزی شبیه به `123456789:ABCDEF...`).  

---
### 🔹 Getting the Chat ID | دریافت Chat ID  
Follow these steps to get your Chat ID:  
برای دریافت Chat ID خود، این مراحل را طی کنید:  

1. Message **[@userinfobot](https://t.me/useridinfobot)** on Telegram.  
   به ربات **[@userinfobot](https://t.me/useridinfobot)** پیام دهید.  
2. Your Chat ID will be displayed.  
   چت آیدی شما نمایش داده خواهد شد.  

---
### 🔹 Configuring `TelegramBot-config.txt` | تنظیم فایل `TelegramBot-config.txt`  
If you need to edit the information, open the `config.txt` file and enter your details as follows:  
اگر نیاز به ویرایش اطلاعات داشتید، می‌توانید فایل `config.txt` را باز کرده و اطلاعات خود را وارد کنید:  

```ini
Device_Name=Your_Device_Name
Device_ID=Your_Device_ID
Bot_Token=Your_Bot_Token
Chat_ID=Your_Chat_ID
```

📌 **Important Notes | نکات مهم:**  
- `Device Name` and `Device ID` must be unique and not repeated.  
  `نام دستگاه` و `شماره دستگاه` باید یکتا باشند و نباید تکراری وارد شوند.  
- If you make a mistake, you can edit the `config.txt` file and correct the details.  
  در صورت بروز اشتباه، می‌توانید فایل `config.txt` را ویرایش کنید و اطلاعات را اصلاح نمایید.  
- **Do not share this file with anyone, as it contains your private information!**  
  **این فایل را با کسی به اشتراک نگذارید، چون اطلاعات خصوصی شما را در خود دارد!**  

---


import time
from datetime import datetime
from bitcoinlib.keys import Key
from bitcoinlib.services.services import Service
import threading
import requests
import socket
import platform
import pytz  # For Iran timezone support

# Counter variables
wallet_count = 0
error_count = 0
found_wallets = 0
last_report_time = time.time()
last_wallet_check_time = time.time()

# 📌 Read BOT_TOKEN and CHAT_ID from TelegramBot-config.txt
def read_config():
    config = {}
    with open("TelegramBot-config.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    return config

config = read_config()
BOT_TOKEN = config.get("BOT_TOKEN")
CHAT_ID = config.get("CHAT_ID")

def send_telegram_message(message, chat_id=CHAT_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def log_message(filename, message):
    with open(filename, "a", encoding="utf-8") as f:  # Ensuring UTF-8 encoding
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
 
def get_ip():
    # Get the system's IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_system_info():
    # Get system information like OS, version, and architecture
    system_info = platform.system()  # Operating system (Windows, Linux, Darwin, ...)
    version_info = platform.version()  # OS version
    architecture = platform.architecture()[0]  # Architecture (32bit or 64bit)
    return f"{system_info} {version_info} ({architecture})"

# Send a start-up message to the Telegram bot
def notify_start():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = get_ip()
    system_info = get_system_info()
    message = f"🟢 Script Started!\n🕰️ Start Time: {start_time}\n🌐 IP Address: {ip_address}\n💻 System Info: {system_info}\n\nUse /status to check the bot status."
    send_telegram_message(message)

# Notify that script has started
notify_start()

# Handle custom commands like /status
def handle_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": -1}
    
    while True:
        try:
            response = requests.get(url, params=params).json()
            for update in response.get("result", []):
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                
                if text == "/status":
                    # Getting system info and IP address when status is requested
                    system_info = get_system_info()
                    ip_address = get_ip()
                    status_message = (
                        "🟢 Bot is running smoothly!\n"
                        "✅ All systems operational!\n\n"
                        f"💻 System Info: {system_info}\n"
                        f"🌐 IP Address: {ip_address}"
                    )
                    send_telegram_message(status_message, chat_id)
                    
                # Update the offset to avoid fetching the same message again
                if 'update_id' in update:
                    params['offset'] = update['update_id'] + 1
                
        except Exception as e:
            print(f"Error while checking for commands: {e}")
            time.sleep(5)  # Retry after 5 seconds in case of an error

# Main wallet checking function
def check_wallet():
    global wallet_count, error_count, found_wallets, last_wallet_check_time

    key = Key()
    private_key_wif = key.wif()
    address = key.address()
    
    print(f"\n🔍 Checking wallet : {address}")

    service = Service()
    balance_btc = None
    
    def fetch_balance():
        nonlocal balance_btc
        balance_btc = service.getbalance(address)
    
    thread = threading.Thread(target=fetch_balance)
    thread.start()
    thread.join(timeout=10)  # 10-second timeout for balance retrieval
    
    if thread.is_alive():
        log_message("error_log.txt", f"Timeout: Balance check took too long - {address}")
        error_count += 1
        return None, private_key_wif, address
    
    wallet_count += 1
    last_wallet_check_time = time.time()  # ⏳ Update last check time
    return balance_btc, private_key_wif, address

def report_status():
    global wallet_count, error_count, found_wallets, last_report_time

    report_message = (
        f"📊 Bot Status Report:\n"
        f"🔹 Wallets Checked: {wallet_count}\n"
        f"❌ Errors Occurred: {error_count}\n"
        f"🎉 Wallets with Balance: {found_wallets}\n"
        f"⏳ Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    send_telegram_message(report_message)
    log_message("report_log.txt", report_message)

    # Reset counters after sending the report
    wallet_count = 0
    error_count = 0
    found_wallets = 0
    last_report_time = time.time()

def check_inactivity():
    global last_wallet_check_time
    if time.time() - last_wallet_check_time >= 3600:  # 3600 seconds = 1 hour
        send_telegram_message("⚠️ Warning: No wallet has been checked for over 1 hour! There might be an issue.")
        last_wallet_check_time = time.time()  # Prevent repeated warnings

def generate_and_check_wallets(delay=0.1):  
    log_message("found_wallets.txt", "=== Script Started ===")
    log_message("error_log.txt", "=== Script Started ===")

    while True:
        try:
            balance_btc, private_key_wif, address = check_wallet()
            
            if balance_btc is None:
                continue  # If balance is unknown, skip
            
            if balance_btc > 0:
                found_wallets += 1
                log_message("found_wallets.txt", f"✅ Private Key: {private_key_wif}, Address: {address}, Balance: {balance_btc} BTC")
                send_telegram_message(f"🎉 Wallet with balance found!\n💰 Balance: {balance_btc} BTC\n🔑 Address: {address}\n🔐 Private Key: {private_key_wif}")
            else:
                print(f"❌ No balance: {address}")
        
        except Exception as e:
            log_message("error_log.txt", f"Error: {str(e)}")
            error_count += 1

        # Send a report every day at specific hours (6 AM, 12 PM, 6 PM, 12 AM Iran time)
        iran_timezone = pytz.timezone('Asia/Tehran')
        current_time = datetime.now(iran_timezone)
        current_hour = current_time.hour

        if current_hour in [6, 12, 18, 24] and (time.time() - last_report_time >= 3600):  # Ensure report is sent at these times
            report_status()

        # Check if processing has slowed down (no wallets checked for over 1 hour)
        check_inactivity()

        time.sleep(delay)

# Start handling commands in a separate thread
threading.Thread(target=handle_commands, daemon=True).start()

# Run the script with a delay of 0.1 seconds
generate_and_check_wallets(delay=0.1)

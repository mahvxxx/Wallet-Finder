@echo off
echo Downloading program files from GitHub repository...
git clone https://github.com/mahvxxx/wallet-founder.git

cd wallet-founder || exit

echo Installing Python dependencies...
python -m ensurepip
python -m pip install --upgrade pip

if exist requirements.txt (
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt not found! Installing dependencies manually...
    python -m pip install bitcoinlib requests
)

echo Setup completed successfully!
pause

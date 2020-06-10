## nmap Telegram bot

### Step 1) Requirements

- Linux / macOS 10 (or Docker)
- Python 3.5+

### Step 2) Install

Run in your console:

```
sudo apt update && sudo apt -y dist-upgrade
sudo apt install -y git python3-venv tor
git clone https://github.com/vahellame/nmap-telegram-bot.git
cd nmap-telegram-bot
```

View and edit `config.py`.

```
python3 -m venv venv
./venv/bin/pip install -U pip 
./venv/bin/pip install -r requirments.txt
```

### Step 3) Running bot

```
./venv/bin/python main.py
```

### WARNING

In some CIS countries, it is impossible to connect to api.telegram.org without a proxy. To solve this problem, `config.py` specifies socks5 for Tor running locally. If your provider has access to api.telegram.org, you can change REQUEST_KWARGS to None and not install Tor.

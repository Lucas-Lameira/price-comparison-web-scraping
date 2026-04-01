# Price Comparison Web Scraper

An automated Python-based web scraper that monitors prices for specific products across multiple hardware retailers (Amazon, Kabum, and Terabyte) and sends you real-time alerts on Telegram when a price drop is detected!

## 🚀 Features

*   **Anti-Bot scraping**: Uses [Playwright](https://playwright.dev/python/) under the hood to load websites just like a real browser, effortlessly bypassing standard Javascript checks and anti-bot measures.
*   **Multi-Site Monitoring**: Out-of-the-box support for Amazon, Kabum, and Terabyte pages with fallback regex logic for flexibility.
*   **Memory Storage**: Keeps track of the last seen prices locally in a `prices.json` file so it accurately knows when a price drops compared to the previous check.
*   **Telegram Integration**: Pings your phone instantly using the Telegram Bot API when a price drop is detected!

## 🛠️ Prerequisites

*   Python 3.8+
*   A free Telegram account to receive the notifications.

## 📦 Setup Instructions

1.  **Clone the Repository** and navigate inside the directory.
2.  **Create a Virtual Environment** and install the dependencies:
    ```bash
    python -m venv .venv
    
    # On Windows:
    .\.venv\Scripts\Activate.ps1
    
    # On Linux/macOS:
    source .venv/bin/activate
    ```
3.  **Install the Requirements**:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```
4.  **Set up the Config File**: 
    The scraper reads target URLs from `config.json`. Ensure the links inside point to the correct product pages, and adjust the `check_interval_seconds` if you want it to check more or less frequently (default is `3600` seconds / 1 hour).
5.  **Set up Telegram Notifications**:
    Follow the Telegram steps below to fill out your `.env` file!

---

## 📱 Setting up the Telegram Bot

To receive notifications on your phone, you need two pieces of information: a **Token** and your **Chat ID**. 

### Step 1. Get the `TELEGRAM_BOT_TOKEN`
1. Open the Telegram app.
2. Search for the user **@BotFather** (look for the verified blue checkmark ✅).
3. Start a chat and send the message: `/newbot`
4. Choose a name and username for your newly created bot.
5. BotFather will reply with a long **HTTP API Token** (e.g., `123456789:ABCdefGHI_jklMNO`).
6. Rename the `.env.example` file to `.env` and paste this token next to `TELEGRAM_BOT_TOKEN`.

### Step 2. Get the `TELEGRAM_CHAT_ID`
1. Start a chat with your newly created bot (BotFather gives you a `t.me/...` link in the message).
2. Send **any message** to the bot (e.g., "Hello!"). *You MUST do this step first, or the next step will fail.*
3. Open a web browser on your computer and navigate to this exact URL (replace `<YOUR_TOKEN>` with the token you just got from Part 1):
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Look at the text response for a section that says `"chat":{"id": 123456789, ...}`. That long number is your `TELEGRAM_CHAT_ID`. *(If the result is completely empty like `[]`, go back and send another message to the bot, then instantly refresh the page).*
5. Paste this number into your `.env` file next to `TELEGRAM_CHAT_ID`.

---

## 🏃 Running the Scraper

Simply fire up the main script! It acts as a continuously running monitor that checks the prices at whatever interval you specified in `config.json`.

```bash
python main.py
```

*Note: Since the program uses an infinite loop, you can safely close it at any time by pressing `Ctrl + C` in the terminal.*
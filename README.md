# Price Comparison Web Scraper ☁️🛒

An automated Python-based web scraper that monitors prices for specific products across multiple hardware retailers (Amazon, Kabum, and Terabyte). Powered by **GitHub Actions**, it runs entirely in the cloud, saves price history to a **Firebase Database**, and sends you real-time alerts on **Telegram** when a price drop is detected!

## 🚀 Features

*   **100% Cloud Automated**: Runs seamlessly in the background on GitHub Actions every hour. No need to keep your PC turned on.
*   **Anti-Bot Scraping**: Uses [Playwright](https://playwright.dev/python/) to load websites just like a real browser, effortlessly bypassing standard Javascript checks and anti-bot measures.
*   **Free Cloud Storage**: Connects to a serverless Firebase Realtime Database to keep track of the last seen prices securely.
*   **Telegram Integration**: Pings your phone instantly using the Telegram Bot API when a price drop is detected!

## 🛠️ Prerequisites

*   A free **GitHub** account to run the Actions automatically.
*   A free **Firebase** account to store the price history.
*   A free **Telegram** account to receive the notifications.

---

## 📦 Local Testing Setup (Optional)

If you want to run or test the code on your own computer before letting the cloud take over:

1.  **Clone the Repository** and navigate inside the directory.
2.  **Create a Virtual Environment** and install the dependencies:
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\Activate.ps1
    # On Linux/macOS:
    source .venv/bin/activate
    ```
3.  **Install Requirements & Browsers**:
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```
4.  **Local Environment Variables:** Rename `.env.example` to `.env` and fill in your secrets (see sections below). Run `python main.py` to test.

---

## ☁️ Cloud Setup Instructions

Follow these 3 easy phases to set up your keys and launch the bot into the cloud.

### Phase 1: Setting up Telegram 📱
We need to get a **Bot Token** and your personal **Chat ID** so the script can text you.
1. Open Telegram and search for **@BotFather** (look for the verified blue checkmark ✅).
2. Start a chat and send the message: `/newbot`
3. Give your bot a name and username. BotFather will reply with an **HTTP API Token**. Save this!
4. Click the link BotFather gives you to start a chat with your new bot and **send it any message** (e.g., "Hello").
5. On your computer browser, go to this URL (replace `<YOUR_TOKEN>` with the token from Step 3):
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
6. Look at the text response for `"chat":{"id": 123456789, ...}`. That number is your **Chat ID**. Save this!

### Phase 2: Setting up your Firebase Database 🗄️
We need a free database to remember the prices between hourly checks.
1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a free project.
2. Under the **Build** menu on the left, click **Realtime Database** and hit "Create Database" (You can select "Start in Test Mode").
3. Copy your database URL from the dashboard (it looks like `https://my-project-123-default-rtdb.firebaseio.com/`). Save this!
4. Go to **Project Settings** (the gear icon on the top left) > **Service Accounts**.
5. Click **Generate new private key**. This will download a `.json` file to your computer. Open it in Notepad/TextEdit and copy the **entire contents of the file**. Save this!

### Phase 3: Launching via GitHub Actions 🚀
We must securely store those 4 pieces of information we just gathered into GitHub so our code can use them.
1. Push this code to a repository on your GitHub account.
2. Go to your repository's page on GitHub.com.
3. Click **Settings** > **Secrets and variables** (on the left sidebar) > **Actions**.
4. Click the green **New repository secret** button and create these 4 secrets exactly:
   * **`TELEGRAM_BOT_TOKEN`**: Paste your token from Phase 1.
   * **`TELEGRAM_CHAT_ID`**: Paste your Chat ID from Phase 1.
   * **`FIREBASE_DATABASE_URL`**: Paste your Database URL from Phase 2.
   * **`FIREBASE_CREDENTIALS_JSON`**: Paste the entire massive block of JSON text from Phase 2.

### You're done! 🎉
GitHub Actions will now automatically wake up and run `.github/workflows/scraper.yml` every hour. It will load Playwright, check the prices across Amazon, Kabum, and Terabyte, save them to Firebase, and text you if there are any deals!
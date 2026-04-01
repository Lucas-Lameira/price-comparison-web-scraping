import json
import os
import time
from datetime import datetime
from scraper import get_current_prices
from notifier import send_telegram_message

PRICES_FILE = "prices.json"
CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_previous_prices():
    if not os.path.exists(PRICES_FILE):
        return {}
    with open(PRICES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_prices(prices_data):
    with open(PRICES_FILE, 'w', encoding='utf-8') as f:
        json.dump(prices_data, f, indent=4)

def check_prices():
    print(f"\n--- Checking prices at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    config = load_config()
    previous_prices = load_previous_prices()
    
    current_prices = get_current_prices(config['products'])
    
    if not current_prices:
        print("No prices found in this run.")
        return

    messages = []
    for store, current_price in current_prices.items():
        prev_price = previous_prices.get(store)
        
        print(f"[{store}] Current: R$ {current_price:.2f} | Previous: {f'R$ {prev_price:.2f}' if prev_price else 'None'}")
        
        if prev_price is not None and current_price < prev_price:
            difference = prev_price - current_price
            msg = f"📉 **PRICE DROP WARNING!** 📉\n\nStore: *{store}*\nNew Price: *R$ {current_price:.2f}*\nOld Price: R$ {prev_price:.2f}\nDrop of: R$ {difference:.2f}!"
            messages.append(msg)
            
            store_url = next((p['url'] for p in config['products'] if p['store'] == store), "")
            if store_url:
                messages.append(f"Link: {store_url}")
                
        previous_prices[store] = current_price

    if messages:
        full_message = "\n\n".join(messages)
        send_telegram_message(full_message)
    else:
        print("No price drops detected.")

    save_prices(previous_prices)

def main():
    print("🚀 Starting Price Monitor Bot...")
    config = load_config()
    interval = config.get("check_interval_seconds", 3600)
    
    print(f"Monitoring prices every {interval} seconds (~{interval/3600:.1f} hours).")
    
    while True:
        try:
            check_prices()
        except Exception as e:
            print(f"An error occurred during check_prices: {e}")
        
        print(f"Sleeping for {interval} seconds...")
        time.sleep(interval)

if __name__ == "__main__":
    main()

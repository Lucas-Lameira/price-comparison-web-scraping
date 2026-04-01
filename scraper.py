from playwright.sync_api import sync_playwright
import re
import time

def extract_price_from_text(text):
    if not text:
        return None

    match = re.search(r'R\$\s*([\d\.]+,\d{2})', text)
    if match:
        price_str = match.group(1).replace('.', '').replace(',', '.')
        try:
            return float(price_str)
        except ValueError:
            return None
    return None

def scrape_amazon(page, url):
    page.goto(url, timeout=60000)
    try:
        page.wait_for_selector('#corePriceDisplay_desktop_feature_div', timeout=10000)
        whole = page.locator('#corePriceDisplay_desktop_feature_div .a-price-whole').first.inner_text()
        fraction = page.locator('#corePriceDisplay_desktop_feature_div .a-price-fraction').first.inner_text()
        if whole and fraction:
             price_str = f"{whole}{fraction}".replace('.', '').replace(',', '.')
             return float(price_str)
    except Exception:
        pass

    text = page.locator('body').inner_text()
    return extract_price_from_text(text)

def scrape_kabum(page, url):
    page.goto(url, timeout=60000)
    try:
        element = page.wait_for_selector('div.finalPrice, h4.finalPrice, h4:has-text("R$")', timeout=10000)
        text = element.inner_text()
        return extract_price_from_text(text)
    except Exception:
        text = page.locator('body').inner_text()
        return extract_price_from_text(text)

def scrape_terabyte(page, url):
    page.goto(url, timeout=60000)
    try:
        element = page.wait_for_selector('#valVista', timeout=10000)
        text = element.inner_text()
        return extract_price_from_text(text)
    except Exception:
        text = page.locator('body').inner_text()
        return extract_price_from_text(text)

def get_current_prices(products):
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for product in products:
            store = product['store']
            url = product['url']
            print(f"Scraping {store}...")
            
            price = None
            try:
                if store.lower() == 'amazon':
                    price = scrape_amazon(page, url)
                elif store.lower() == 'kabum':
                    price = scrape_kabum(page, url)
                elif store.lower() == 'terabyte':
                    price = scrape_terabyte(page, url)
                else:
                    print(f"Unknown store: {store}")
            except Exception as e:
                print(f"Error scraping {store}: {e}")

            if price is not None:
                results[store] = price
                print(f"Found price for {store}: R$ {price:.2f}")
            else:
                print(f"Could not extract price for {store}")
            
            time.sleep(3)

        browser.close()
    return results

if __name__ == "__main__":
    test_products = [
        {"store": "Amazon", "url": "https://www.amazon.com.br/KF432C16BB-Mem%C3%B3ria-3200Mhz-desktop-gamers/dp/B097K5J1SB/ref=sr_1_3"},
    ]
    prices = get_current_prices(test_products)
    print("Test Results:", prices)

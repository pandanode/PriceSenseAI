import re
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------------------------------------
# MINIMUM PRICE FILTER
# -------------------------------------------------------
MIN_PRICE = 1  # ₹


# -------------------------------------------------------
# DRIVER SETUP
# -------------------------------------------------------

def create_driver():
    """Create a stealthy Chrome browser instance"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # ✅ Railway/Linux Chrome path detection
    if os.path.exists("/usr/bin/chromium"):
        options.binary_location = "/usr/bin/chromium"
    elif os.path.exists("/usr/bin/chromium-browser"):
        options.binary_location = "/usr/bin/chromium-browser"
    elif os.path.exists("/usr/bin/google-chrome"):
        options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


# -------------------------------------------------------
# RELEVANCE CHECKER
# -------------------------------------------------------

def is_relevant(title: str, product_name: str) -> bool:
    if not title or title == "N/A":
        return False

    title_lower = title.lower()
    keywords = product_name.lower().split()

    matched = 0
    for word in keywords:
        if word.isdigit():
            if re.search(rf'\b{re.escape(word)}\b', title_lower):
                matched += 1
        else:
            if word in title_lower:
                matched += 1

    return (matched / len(keywords)) >= 0.4


# -------------------------------------------------------
# AMAZON SCRAPER
# -------------------------------------------------------

def scrape_amazon(product_name: str, driver):
    try:
        url = f"https://www.amazon.in/s?k={book_name.replace(' ', '+')}"
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
            )
        )
        time.sleep(2)

        results = driver.find_elements(
            By.CSS_SELECTOR, "div[data-component-type='s-search-result']"
        )

        for result in results[:15]:
            title = "N/A"
            try:
                title = result.find_element(By.CSS_SELECTOR, "h2").text.strip()
            except:
                pass

            try:
                price_text = result.find_element(
                    By.CSS_SELECTOR, "span.a-price-whole"
                ).text
                price = float(price_text.replace(",", "").strip())
            except:
                continue

            if price < MIN_PRICE:
                continue

            if not is_relevant(title, product_name):
                print(f"   ⚠️  Amazon skipping: {title[:65]}")
                continue

            product_url = "N/A"
            try:
                link = result.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline")
                product_url = link.get_attribute("href")
            except:
                pass

            return {"platform": "Amazon", "title": title, "price": price, "url": product_url}

        return None

    except Exception as e:
        print(f"[Amazon Error] {e}")
        return None


# -------------------------------------------------------
# FLIPKART SCRAPER
# -------------------------------------------------------

def scrape_flipkart(product_name: str, driver):
    try:
        url = f"https://www.flipkart.com/search?q={book_name.replace(' ', '+')}"
        driver.get(url)
        time.sleep(4)

        for xpath in [
            "//button[contains(text(),'✕')]",
            "//button[contains(@class,'_2KpZ6l')]",
        ]:
            try:
                btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                time.sleep(1)
                break
            except:
                continue

        title_elements = driver.find_elements(By.XPATH, "//a[contains(@class,'pIpigb')]")

        for title_el in title_elements[:15]:
            title = "N/A"
            try:
                title = title_el.text.strip()
            except:
                pass

            if not title or title == "N/A":
                continue

            price = None
            try:
                price_text = title_el.find_element(
                    By.XPATH, "following::div[contains(@class,'hZ3P6w')][1]"
                ).text
                price = float(price_text.replace("₹", "").replace(",", "").strip())
            except:
                continue

            if not price or price < MIN_PRICE:
                continue

            if not is_relevant(title, book_name):
                print(f"   ⚠️  Flipkart skipping: {title[:65]}")
                continue

            product_url = "N/A"
            try:
                href = title_el.get_attribute("href")
                product_url = ("https://www.flipkart.com" + href
                               if href.startswith("/") else href)
            except:
                pass

            return {"platform": "Flipkart", "title": title, "price": price, "url": product_url}

        return None

    except Exception as e:
        print(f"[Flipkart Error] {e}")
        return None


# -------------------------------------------------------
# SNAPDEAL SCRAPER
# -------------------------------------------------------

def scrape_snapdeal(product_name: str, driver):
    try:
        url = f"https://www.snapdeal.com/search?keyword={book_name.replace(' ', '%20')}"
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tuple-listing"))
        )
        time.sleep(2)

        results = driver.find_elements(By.CSS_SELECTOR, "div.product-tuple-listing")

        for result in results[:15]:
            try:
                title = result.find_element(By.CSS_SELECTOR, "p.product-title").text.strip()
            except:
                continue

            try:
                price_text = result.find_element(
                    By.CSS_SELECTOR, "span.product-price"
                ).text
                price = float(
                    price_text.replace("Rs.", "").replace("₹", "")
                    .replace(",", "").strip()
                )
            except:
                continue

            if price < MIN_PRICE:
                continue

            if not is_relevant(title, book_name):
                print(f"   ⚠️  Snapdeal skipping: {title[:65]}")
                continue

            product_url = "N/A"
            try:
                link = result.find_element(By.CSS_SELECTOR, "a.dp-widget-link")
                product_url = link.get_attribute("href")
            except:
                pass

            return {"platform": "Snapdeal", "title": title, "price": price, "url": product_url}

        return None

    except Exception as e:
        print(f"[Snapdeal Error] {e}")
        return None


# -------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------

def get_all_prices(product_name: str):
    print(f"\n📚 Searching for: {book_name}")
    print("⏳ Opening browser...\n")

    driver = create_driver()
    results = []

    try:
        amazon_data = scrape_amazon(book_name, driver)
        if amazon_data:
            results.append(amazon_data)
            print(f"✅ Amazon   : ₹{amazon_data['price']:,.0f} — {amazon_data['title'][:60]}")
        else:
            print("❌ Amazon   : No result found")

        flipkart_data = scrape_flipkart(book_name, driver)
        if flipkart_data:
            results.append(flipkart_data)
            print(f"✅ Flipkart : ₹{flipkart_data['price']:,.0f} — {flipkart_data['title'][:60]}")
        else:
            print("❌ Flipkart : No result found")

        snapdeal_data = scrape_snapdeal(book_name, driver)
        if snapdeal_data:
            results.append(snapdeal_data)
            print(f"✅ Snapdeal : ₹{snapdeal_data['price']:,.0f} — {snapdeal_data['title'][:60]}")
        else:
            print("❌ Snapdeal : No result found")

    finally:
        driver.quit()

    print("\n" + "=" * 55)
    if results:
        best = min(results, key=lambda x: x["price"])
        worst = max(results, key=lambda x: x["price"])
        saving = worst["price"] - best["price"]
        print(f"🏆 Best Deal : {best['platform']} at ₹{best['price']:,.0f}")
        print(f"💰 You Save  : ₹{saving:,.0f} vs {worst['platform']}")
    else:
        print("⚠️  No results found.")

    return results


if __name__ == "__main__":

    get_all_prices("Python Crash Course")

    get_all_prices("Python Crash Course")


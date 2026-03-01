import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.flipkart.com/search?q=Python+Crash+Course&category=bks")
time.sleep(4)

# Close popup
try:
    driver.find_element("xpath", "//button[contains(text(),'✕')]").click()
    time.sleep(1)
except:
    pass

soup = BeautifulSoup(driver.page_source, "html.parser")

print("=" * 60)
print("🔍 TITLES")
print("=" * 60)
for tag in soup.find_all(string=lambda t: t and "Python" in t)[:8]:
    p = tag.parent
    print(f"<{p.name}> class={p.get('class')} | {tag.strip()[:60]}")

print("\n" + "=" * 60)
print("🔍 PRICES")
print("=" * 60)
for tag in soup.find_all(string=lambda t: t and "₹" in t)[:8]:
    p = tag.parent
    print(f"<{p.name}> class={p.get('class')} | {tag.strip()[:40]}")

driver.quit()

print("\n" + "=" * 60)
print("🔍 ALL DIVS/SPANS NEAR FIRST PRODUCT")
print("=" * 60)

# Find first product link and look at its parent containers
first_link = soup.find("a", class_="pIpigb")
if first_link:
    # Walk up 5 levels and print all children
    container = first_link
    for _ in range(5):
        container = container.parent
    
    # Print all tags inside this container
    for tag in container.find_all(["div", "span"]):
        text = tag.get_text(strip=True)
        if text and len(text) < 50 and tag.get("class"):
            print(f"<{tag.name}> class={tag.get('class')} | '{text}'")
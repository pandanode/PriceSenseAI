import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
driver.get("https://www.snapdeal.com/search?keyword=Samsung+Galaxy+S24&sort=rlvncy")
time.sleep(5)

with open("snapdeal_page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

print("✅ Page saved to snapdeal_page.html")
print(f"📄 Page title: {driver.title}")
print(f"📄 Current URL: {driver.current_url}")
driver.quit()
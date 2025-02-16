import os

print("FB_EMAIL:", os.getenv("FB_EMAIL"))
print("FB_PASSWORD:", os.getenv("FB_PASSWORD"))
print("GROUP_URL:", os.getenv("GROUP_URL"))
print("PAGE_URL:", os.getenv("PAGE_URL"))

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# استرجاع القيم من متغيرات البيئة
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
PAGE_URL = os.getenv("PAGE_URL")
GROUP_URL = os.getenv("GROUP_URL")

# تأكد من أن جميع المتغيرات موجودة
if not all([FB_EMAIL, FB_PASSWORD, PAGE_URL, GROUP_URL]):
    raise ValueError("يرجى ضبط جميع متغيرات البيئة المطلوبة.")

# إعداد Selenium
options = Options()
options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    driver.get("https://www.facebook.com/")
    time.sleep(3)
    driver.find_element(By.ID, "email").send_keys(FB_EMAIL)
    driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
    driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)
    time.sleep(5)
    print("✅ تم تسجيل الدخول بنجاح!")

def post_to_group():
    driver.get(GROUP_URL)
    time.sleep(5)
    
    try:
        post_box = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
        post_box.click()
        time.sleep(2)
        post_box.send_keys("هذا منشور تجريبي من البوت! 🤖")
        time.sleep(2)
        post_box.send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(5)
        print("✅ تم نشر المنشور في المجموعة!")
    except Exception as e:
        print(f"❌ فشل النشر: {e}")

if __name__ == "__main__":
    try:
        login()
        post_to_group()
    finally:
        driver.quit()

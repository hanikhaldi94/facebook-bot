import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
GROUP_URL = os.getenv("GROUP_URL")
PAGE_URL = os.getenv("PAGE_URL")
POST_CONTENT = os.getenv("POST_CONTENT")


print(f"FB_EMAIL: {FB_EMAIL}")
print(f"FB_PASSWORD: {FB_PASSWORD}")
print(f"GROUP_URL: {GROUP_URL}")
print(f"PAGE_URL: {PAGE_URL}")
print(f"POST_CONTENT: {POST_CONTENT}")


if not all([FB_EMAIL, FB_PASSWORD, GROUP_URL, PAGE_URL, POST_CONTENT]):
    raise ValueError("❌ يرجى ضبط جميع متغيرات البيئة المطلوبة.")

# إعداد المتصفح (Google Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# تسجيل الدخول إلى Facebook
def login():
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    driver.find_element(By.ID, "email").send_keys(FB_EMAIL)
    driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
    driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)
    
    time.sleep(5)  # انتظار تحميل الصفحة بعد تسجيل الدخول

    print("✅ تم تسجيل الدخول بنجاح!")

# نشر منشور في مجموعة
def post_to_group():
    driver.get(GROUP_URL)
    time.sleep(5)

    try:
        post_box = driver.find_element(By.XPATH, "//div[@role='textbox']")
        post_box.click()
        time.sleep(2)

        post_box.send_keys(POST_CONTENT)
        time.sleep(2)

        post_button = driver.find_element(By.XPATH, "//div[@aria-label='Post']")
        post_button.click()
        
        time.sleep(5)
        print("✅ تم نشر المنشور في المجموعة بنجاح!")

    except Exception as e:
        print(f"❌ فشل نشر المنشور: {e}")

# تنفيذ البوت
if __name__ == "__main__":
    try:
        login()
        post_to_group()
    finally:
        driver.quit()

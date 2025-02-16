import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# تحميل المتغيرات البيئية
load_dotenv()

FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")

# التأكد من تحميل القيم
if not FB_EMAIL or not FB_PASSWORD:
    raise ValueError("⚠️ خطأ: لم يتم تحميل FB_EMAIL أو FB_PASSWORD بشكل صحيح!")

# إعداد خيارات المتصفح
options = Options()
options.add_argument("--headless")  # تشغيل بدون واجهة
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# تشغيل WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    """تسجيل الدخول إلى Facebook"""
    driver.get("https://www.facebook.com/")

    # الانتظار حتى يتم تحميل الصفحة
    time.sleep(3)

    # البحث عن حقول الإدخال وإدخال البيانات
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "pass")
    login_button = driver.find_element(By.NAME, "login")

    email_input.send_keys(FB_EMAIL)
    password_input.send_keys(FB_PASSWORD)
    login_button.click()

    # الانتظار قليلاً بعد تسجيل الدخول
    time.sleep(5)
    print("✅ تم تسجيل الدخول بنجاح!")

# تنفيذ عملية تسجيل الدخول
try:
    login()
except Exception as e:
    print(f"❌ خطأ أثناء تسجيل الدخول: {e}")
finally:
    driver.quit()

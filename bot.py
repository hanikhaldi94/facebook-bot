
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# جلب المتغيرات من بيئة Railway
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
PAGE_URL = os.getenv("PAGE_URL")
GROUP_URL = os.getenv("GROUP_URL")

# إعداد المتصفح
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # تشغيل بدون واجهة
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    """تسجيل الدخول إلى فيسبوك"""
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    driver.find_element(By.ID, "email").send_keys(FB_EMAIL)
    driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
    driver.find_element(By.NAME, "login").click()
    time.sleep(5)

def switch_to_page():
    """التبديل إلى الصفحة الإدارية"""
    driver.get(PAGE_URL)
    time.sleep(5)

def post_to_group():
    """النشر في المجموعة باستخدام الصفحة"""
    driver.get(GROUP_URL)
    time.sleep(5)

    # البحث عن مربع الكتابة
    post_box = driver.find_element(By.CSS_SELECTOR, '[aria-label="اكتب شيئًا..."]')
    post_box.click()
    time.sleep(2)

    # كتابة المنشور
    post_box.send_keys("🚀 هذا منشور تلقائي من صفحتي!")
    time.sleep(2)

    # النقر على زر النشر
    post_button = driver.find_element(By.XPATH, '//span[contains(text(),"نشر")]')
    post_button.click()
    time.sleep(5)

    print("✅ تم النشر بنجاح!")

# تشغيل البوت
login()
switch_to_page()
post_to_group()

driver.quit()

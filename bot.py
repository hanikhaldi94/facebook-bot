import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# ✅ جلب متغيرات البيئة من Railway
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
GROUP_URL = os.getenv("GROUP_URL")
PAGE_URL = os.getenv("PAGE_URL")
POST_CONTENT = os.getenv("POST_CONTENT", "هذا منشور تلقائي من البوت 🤖")

# ✅ التأكد من أن جميع المتغيرات موجودة
if not all([FB_EMAIL, FB_PASSWORD, GROUP_URL, PAGE_URL]):
    raise ValueError("❌ يرجى ضبط جميع متغيرات البيئة المطلوبة.")

# ✅ إعداد Selenium وتشغيل المتصفح في وضع التخفي
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # تشغيل المتصفح بدون واجهة (للسيرفرات)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x800")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ تشغيل WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    """ تسجيل الدخول إلى Facebook """
    driver.get("https://www.facebook.com/login")
    time.sleep(2)
    
    driver.find_element(By.ID, "email").send_keys(FB_EMAIL)
    driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
    driver.find_element(By.ID, "pass").send_keys(Keys.RETURN)
    time.sleep(5)

    # ✅ التحقق من نجاح تسجيل الدخول
    if "login_attempt" in driver.current_url:
        raise ValueError("❌ فشل تسجيل الدخول! تأكد من صحة البريد وكلمة المرور.")

    print("✅ تم تسجيل الدخول بنجاح!")

def post_to_page():
    """ نشر منشور في الصفحة """
    driver.get(PAGE_URL)
    time.sleep(5)
    
    try:
        post_box = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'إنشاء منشور')]")
        post_box.click()
        time.sleep(3)
        
        active_box = driver.switch_to.active_element
        active_box.send_keys(POST_CONTENT)
        time.sleep(2)
        
        post_button = driver.find_element(By.XPATH, "//div[@aria-label='نشر']")
        post_button.click()
        time.sleep(5)
        
        print("✅ تم نشر المنشور على الصفحة!")

    except Exception as e:
        print(f"❌ فشل النشر في الصفحة: {e}")

def post_to_group():
    """ نشر منشور في المجموعة """
    driver.get(GROUP_URL)
    time.sleep(5)
    
    try:
        post_box = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'إنشاء منشور')]")
        post_box.click()
        time.sleep(3)
        
        active_box = driver.switch_to.active_element
        active_box.send_keys(POST_CONTENT)
        time.sleep(2)
        
        post_button = driver.find_element(By.XPATH, "//div[@aria-label='نشر']")
        post_button.click()
        time.sleep(5)
        
        print("✅ تم نشر المنشور في المجموعة!")

    except Exception as e:
        print(f"❌ فشل النشر في المجموعة: {e}")

# ✅ تشغيل البوت
login()
post_to_page()
post_to_group()

# ✅ إغلاق المتصفح
driver.quit()
print("✅ تم إنهاء البرنامج بنجاح!")

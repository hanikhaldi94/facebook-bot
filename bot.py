import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ جلب متغيرات البيئة
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASSWORD = os.getenv("FB_PASSWORD")
GROUP_URL = os.getenv("GROUP_URL")
PAGE_URL = os.getenv("PAGE_URL")
POST_CONTENT = "هذا منشور تجريبي من البوت 🚀"

# ✅ التحقق من أن جميع المتغيرات مضبوطة
if not all([FB_EMAIL, FB_PASSWORD, GROUP_URL, PAGE_URL]):
    raise ValueError("❌ يرجى ضبط جميع متغيرات البيئة المطلوبة.")

# ✅ إعداد متصفح Chrome للعمل بدون واجهة رسومية (Headless Mode)
chrome_options = Options()
chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ تشغيل المتصفح
service = Service("/usr/bin/chromedriver")  # تأكد من أن chromedriver مثبت
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ✅ تسجيل الدخول إلى فيسبوك
    driver.get("https://www.facebook.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(FB_EMAIL)
    driver.find_element(By.ID, "pass").send_keys(FB_PASSWORD)
    driver.find_element(By.NAME, "login").click()
    print("✅ تم تسجيل الدخول بنجاح!")

    # ✅ الذهاب إلى المجموعة
    time.sleep(5)  # انتظار تحميل الصفحة
    driver.get(GROUP_URL)
    print("🔹 فتح المجموعة:", GROUP_URL)

    # ✅ الانتظار حتى يظهر مربع الكتابة
    wait = WebDriverWait(driver, 10)
    post_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))

    # ✅ كتابة المنشور وإرساله
    post_box.click()
    post_box.send_keys(POST_CONTENT)
    time.sleep(2)  # انتظار قليل
    post_box.send_keys(Keys.CONTROL, Keys.ENTER)  # إرسال المنشور
    print("✅ تم نشر المنشور بنجاح!")

except Exception as e:
    print("❌ حدث خطأ:", str(e))

finally:
    driver.quit()  # ✅ إغلاق المتصفح

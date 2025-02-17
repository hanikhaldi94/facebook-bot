import json
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ كوكيز فيسبوك الحقيقية (حاليًا للتجريب فقط)
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "xs", "value": "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False}
]

# ✅ رابط الصفحة التي تديرها
PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717"

# ✅ رابط المجموعة التي يمكن للصفحة النشر فيها
GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"

# ✅ محتوى المنشور
POST_CONTENT = "🚀 هذا منشور تجريبي للنشر التلقائي!"

# إعداد WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")

# تخصيص مجلد مؤقت لمتصفح كروم
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # فتح فيسبوك وتحميل الكوكيز
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # الانتقال إلى الصفحة للتحقق من تسجيل الدخول
    driver.get(PAGE_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # الانتقال إلى المجموعة
    driver.get(GROUP_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]')))

    # البحث عن مربع النص وإدخال المحتوى
    post_box = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
    post_box.send_keys(POST_CONTENT)

    # انتظار زر "نشر" والضغط عليه
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))).click()

    # الانتظار قليلاً للتأكد من نجاح النشر
    time.sleep(5)

    print("✅ تم نشر المنشور بنجاح!")

except Exception as e:
    print(f"❌ خطأ أثناء التشغيل: {e}")

finally:
    driver.quit()

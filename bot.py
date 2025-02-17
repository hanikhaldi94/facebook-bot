from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# استبدل هنا بالكود الخاص بك
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "xs", "value": "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False}
]
GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717"
POST_CONTENT = "هذا هو المحتوى الذي سيتم نشره في المجموعة."

# إعداد الـ WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # لتشغيل المتصفح بدون واجهة رسومية
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# تحميل الكوكيز
driver.get("https://www.facebook.com/")
for cookie in FB_COOKIES:
    driver.add_cookie(cookie)

# الانتقال إلى صفحة المجموعة
driver.get(GROUP_URL)

# زيادة الوقت المسموح به للانتظار
try:
    # الانتظار حتى تظهر نافذة الكتابة
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]'))
    )

    # العثور على مربع النص والكتابة فيه
    post_box = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
    post_box.send_keys(POST_CONTENT)

    # الضغط على زر النشر
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))
    ).click()

    # الانتظار قليلاً للتحقق من النشر
    time.sleep(3)

    # استخراج الـ ID المنشور من الرابط
    post_url = driver.current_url

    # طباعة نتائج النشر
    if post_url:
        print(f"تم نشر المنشور بنجاح! رابط المنشور: {post_url}")
    else:
        print("لم يتم نشر المنشور.")

except Exception as e:
    print(f"حدث خطأ: {e}")

# إغلاق المتصفح
driver.quit()

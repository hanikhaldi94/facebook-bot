import os
import shutil
import uuid
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# استبدال البيانات في الكوكيز
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "datr", "value": "xerKZkgrzmFkzN468jcjg76L", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "fr", "value": "1uHf2lvHJbQdZ3xbn.AWW9Ig0LIu3idsSiBUed3IFoWKOaR6EID3_Q6w.BnsuUO..AAA.0.0.BnsxHl.AWWOKwkesnM", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "i_user", "value": "61564136097717", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "ps_l", "value": "1", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "ps_n", "value": "1", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "sb", "value": "xerKZpIySD7K9J_v7IYZxnaM", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "wd", "value": "1920x953", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "XS", "value": "36%3A8ml2jGQRRpfEaA%3A2%3A1739786751%3A-1%3A1051", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False}
]

GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717"
POST_CONTENT = "هذا هو المحتوى الذي سيتم نشره في المجموعة."

# إعداد الـ WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # لتشغيل المتصفح بدون واجهة رسومية
options.add_argument("--no-sandbox")  # لتجنب مشاكل في بيئات الحاويات مثل Docker

# تحديد مجلد بيانات المستخدم الفريد باستخدام uuid لضمان أنه لا يتكرر
user_data_dir = f"/tmp/chrome_user_data_{uuid.uuid4().hex}"

# حذف المجلد إذا كان موجودًا من الجلسات السابقة
if os.path.exists(user_data_dir):
    shutil.rmtree(user_data_dir)  # احذف المجلد وجميع محتوياته

os.makedirs(user_data_dir)  # إنشاء المجلد الفريد

options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# تحميل الكوكيز
driver.get("https://www.facebook.com/")  # فتح الفيسبوك أولاً
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

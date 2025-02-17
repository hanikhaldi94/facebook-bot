import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# بيانات الكوكيز (تأكد من تحديثها عند الحاجة)
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "xs", "value": "36%3A8ml2jGQRRpfEaA%3A2%3A1739786751%3A-1%3A1051", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False}
]

GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
POST_CONTENT = "هذا هو المحتوى الذي سيتم نشره في المجموعة."

# 🔹 إعداد الـ WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
options.add_argument("--remote-debugging-port=9222")  
options.add_argument("--incognito")
options.add_argument("--disable-extensions")

# 🔹 إنشاء مجلد مؤقت للـ `user-data-dir` لتجنب أخطاء الجلسة
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

# 🔹 تشغيل WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # ✅ فتح الفيسبوك
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # ✅ تحميل الكوكيز
    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # ✅ تحديث الصفحة بعد تحميل الكوكيز
    driver.refresh()
    time.sleep(5)

    # ✅ الانتقال إلى صفحة المجموعة
    driver.get(GROUP_URL)

    # ✅ الانتظار حتى تظهر نافذة الكتابة
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]'))
    )

    # ✅ العثور على مربع النص والكتابة فيه
    post_box = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
    post_box.send_keys(POST_CONTENT)

    # ✅ الضغط على زر النشر
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))
    ).click()

    # ✅ الانتظار قليلاً للتحقق من النشر
    time.

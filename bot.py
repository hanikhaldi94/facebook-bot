import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# تعريف الكوكيز الخاصة بفيسبوك (استبدل القيم بكوكيزك الفعلية)
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "xs", "value": "24%3AOtkShu0keCrL3A%3A2%3A1739742595%3A-1%3A1051%3A%3AAcU55dwuLfb9kOjznYaChsdoykCbrAYMnTaEBERD1Q", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "fr", "value": "1g9dQxf6nkkx1mqfL.AWUxTSE8S0iNwwdkqR958d8_sl1ogzjNtJRR9Q.Bns28q..AAA.0.0.Bns28q.AWVRew9xDFU", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "sb", "value": "x31rZRY5h2hhr5cT5N3xs_sR", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "datr", "value": "_X1rZXLEnaiQ1InGXamm_2lM", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
]

# الرابط الخاص بالصفحة والمجموعة
PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717"
GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
POST_CONTENT = "هذا هو المحتوى الذي سيتم نشره في المجموعة."

# إعدادات WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920x1080")  # ضبط نافذة المتصفح

# استخدام مجلد مؤقت لتخزين البيانات
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--headless")  # إذا كنت تحتاج إلى تشغيل المتصفح بدون واجهة

# تشغيل المتصفح
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # فتح صفحة فيسبوك وتسجيل الدخول باستخدام الكوكيز
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # الانتقال إلى صفحة الحساب الشخصية
    driver.get(PAGE_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # انتظار التحميل الكامل للصفحة
    time.sleep(5)

    # التبديل إلى الصفحة (إن كانت هذه هي صفحة المستخدم)
    try:
        switch_button = driver.find_element(By.XPATH, '//div[contains(text(),"تبديل الآن")]')
        switch_button.click()
        time.sleep(5)
        print("تم التبديل إلى الصفحة بنجاح.")
    except Exception as e:
        print(f"❌ خطأ أثناء التبديل للصفحة: {e}")

    # الانتقال إلى المجموعة والنشر
    driver.get(GROUP_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]')))
    post_box = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
    post_box.send_keys(POST_CONTENT)

    # الضغط على زر النشر
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))).click()

    time.sleep(5)  # الانتظار قليلاً للتأكد من نشر المنشور
    print("تم نشر المنشور بنجاح!")

except Exception as e:
    print(f"❌ خطأ أثناء التشغيل: {e}")

finally:
    if 'driver' in locals():
        driver.quit()

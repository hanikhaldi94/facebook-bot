import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# تعريف الكوكيز (مباشرة للاختبار)
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "xs", "value": "24%3AOtkShu0keCrL3A%3A2%3A1739742595%3A-1%3A1051%3A%3AAcU55dwuLfb9kOjznYaChsdoykCbrAYMnTaEBERD1Q", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "fr", "value": "1g9dQxf6nkkx1mqfL.AWUxTSE8S0iNwwdkqR958d8_sl1ogzjNtJRR9Q.Bns28q..AAA.0.0.Bns28q.AWVRew9xDFU", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "sb", "value": "x31rZRY5h2hhr5cT5N3xs_sR", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
    {"name": "datr", "value": "_X1rZXLEnaiQ1InGXamm_2lM", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False},
]

# الروابط المستهدفة
PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717"
GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
POST_CONTENT = "🚀 هذا منشور تجريبي للنشر التلقائي!"

# إعداد WebDriver
options = webdriver.ChromeOptions()
# ✅ أضف هذه الخيارات لحل مشكلة "tab crashed"
options.add_argument("--disable-gpu")  # تعطيل كرت الشاشة الافتراضي
options.add_argument("--disable-dev-shm-usage")  # تحسين استخدام الذاكرة
options.add_argument("--disable-software-rasterizer")  # تعطيل معالجة الرسوميات البرمجية
options.add_argument("--no-sandbox")  # ضروري عند التشغيل على Railway
options.add_argument("--headless")  # تشغيل المتصفح بدون واجهة (يمكن تعطيله للاختبار)

# تشغيل المتصفح
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # فتح فيسبوك وتحميل الكوكيز
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # الانتقال إلى صفحة الفيسبوك
    driver.get(PAGE_URL)
    time.sleep(3)  # انتظار تحميل الصفحة

    # الانتقال إلى المجموعة
    driver.get(GROUP_URL)
    time.sleep(3)

    try:
        # انتظار مربع الكتابة
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]')))
        post_box = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
        post_box.send_keys(POST_CONTENT)

        # انتظار زر النشر والضغط عليه
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))).click()

        time.sleep(5)  # انتظار تأكيد النشر
        print("✅ تم نشر المنشور بنجاح!")

    except Exception as e:
        print(f"❌ خطأ أثناء النشر: {e}")

except Exception as e:
    print(f"❌ خطأ أثناء التشغيل: {e}")

finally:
    driver.quit()

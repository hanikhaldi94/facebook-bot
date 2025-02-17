import time
import tempfile
import os
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
POST_CONTENT = "🚀 هذا منشور تجريبي للنشر التلقائي!"

# إعدادات WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-crash-reporter")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--headless=new")  # تشغيل المتصفح بدون واجهة

# إنشاء مجلد مؤقت فريد لكل جلسة
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

# تشغيل المتصفح
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # فتح فيسبوك وتسجيل الدخول بالكوكيز
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # تحديث الصفحة بعد إضافة الكوكيز
    driver.refresh()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # الانتقال إلى صفحة الحساب الشخصية
    driver.get(PAGE_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # التبديل إلى الصفحة (باستخدام JavaScript بدلاً من XPath)
    try:
        time.sleep(5)  # انتظار تحميل الصفحة بالكامل

        switch_button_js = """
            let buttons = document.querySelectorAll('span');
            for (let btn of buttons) {
                if (btn.innerText.includes('تبديل الآن')) {
                    btn.click();
                    return true;
                }
            }
            return false;
        """
        switched = driver.execute_script(switch_button_js)
        if switched:
            print("✅ تم التبديل إلى الصفحة بنجاح.")
        else:
            print("⚠️ لم يتم العثور على زر التبديل.")
        
        time.sleep(5)  # التأكد من اكتمال العملية

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
    print("✅ تم نشر المنشور بنجاح!")

except Exception as e:
    print(f"❌ خطأ أثناء التشغيل: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
    # تنظيف مجلد البيانات المؤقت بعد الانتهاء
    if os.path.exists(user_data_dir):
        os.rmdir(user_data_dir)

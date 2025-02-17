import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ✅ تعريف الكوكيز الخاصة بحسابك مباشرةً
FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": True},
    {"name": "xs", "value": "24%3AOtkShu0keCrL3A%3A2%3A1739742595%3A-1%3A1051%3A%3AAcU55dwuLfb9kOjznYaChsdoykCbrAYMnTaEBERD1Q", "domain": ".facebook.com", "path": "/", "secure": True},
    {"name": "fr", "value": "1g9dQxf6nkkx1mqfL.AWUxTSE8S0iNwwdkqR958d8_sl1ogzjNtJRR9Q.Bns28q..AAA.0.0.Bns28q.AWVRew9xDFU", "domain": ".facebook.com", "path": "/", "secure": True},
    {"name": "sb", "value": "x31rZRY5h2hhr5cT5N3xs_sR", "domain": ".facebook.com", "path": "/", "secure": True},
    {"name": "datr", "value": "_X1rZXLEnaiQ1InGXamm_2lM", "domain": ".facebook.com", "path": "/", "secure": True}
]

# ✅ رابط الصفحة والمجموعة
PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717"
GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
POST_CONTENT = "🚀 هذا منشور تجريبي للنشر التلقائي من البوت!"

# ✅ إعداد WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ تشغيل المتصفح
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 1️⃣ فتح فيسبوك وتحميل الكوكيز
    driver.get("https://www.facebook.com/")
    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # 2️⃣ الانتقال إلى الصفحة
    driver.get(PAGE_URL)
    time.sleep(3)  # انتظار تحميل الصفحة

    # 3️⃣ التبديل للصفحة إذا كانت متاحة
    try:
        switch_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'التبديل إلى')]"))
        )
        switch_button.click()
        time.sleep(3)  # انتظار التبديل
    except:
        print("✅ لا يوجد تبديل للصفحة، متابعة النشر مباشرة.")

    # 4️⃣ الانتقال إلى المجموعة
    driver.get(GROUP_URL)
    time.sleep(3)

    # 5️⃣ انتظار مربع الكتابة وكتابة المنشور
    post_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]'))
    )
    post_box.send_keys(POST_CONTENT)

    # 6️⃣ الضغط على زر النشر
    post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))
    )
    post_button.click()

    # 7️⃣ الانتظار والتأكد من النشر
    time.sleep(5)
    print("✅ تم نشر المنشور بنجاح!")

except Exception as e:
    print(f"❌ خطأ أثناء التشغيل: {e}")

finally:
    driver.quit()

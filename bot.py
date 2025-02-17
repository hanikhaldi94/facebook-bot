import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ✅ جلب متغيرات البيئة
FB_COOKIES = os.getenv("FB_COOKIES")  # الكوكيز كـ JSON
GROUP_URL = os.getenv("GROUP_URL")
PAGE_URL = os.getenv("PAGE_URL")
POST_CONTENT = os.getenv("POST_CONTENT", "🚀 هذا منشور تجريبي!")

# ✅ التحقق من المتغيرات
if not all([FB_COOKIES, GROUP_URL, PAGE_URL]):
    raise ValueError("❌ يرجى ضبط جميع متغيرات البيئة المطلوبة.")

# ✅ إعداد متصفح Chrome بدون واجهة رسومية (Headless Mode)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ تشغيل المتصفح
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ✅ فتح فيسبوك
    driver.get("https://www.facebook.com")
    time.sleep(3)

    # ✅ تحميل الكوكيز باستخدام JavaScript
    cookie_script = """
    let cookies = JSON.parse(arguments[0]);
    cookies.forEach(cookie => {
        document.cookie = `${cookie.name}=${cookie.value}; domain=${cookie.domain}; path=${cookie.path}; ${cookie.secure ? "Secure;" : ""} ${cookie.httpOnly ? "HttpOnly;" : ""}`;
    });
    """
    driver.execute_script(cookie_script, FB_COOKIES)
    
    print("✅ تم تحميل الكوكيز بنجاح!")

    # ✅ إعادة تحميل الصفحة بعد إدخال الكوكيز
    driver.refresh()
    time.sleep(5)

    # ✅ الذهاب إلى المجموعة
    driver.get(GROUP_URL)
    print("🔹 فتح المجموعة:", GROUP_URL)
    time.sleep(5)

    # ✅ إدخال النص في المنشور بطريقة طبيعية
    post_script = """
    let postBox = document.querySelector('[role="textbox"]');
    if (postBox) {
        postBox.focus();
        let inputEvent = new InputEvent('input', { bubbles: true });
        postBox.innerText = arguments[0];
        postBox.dispatchEvent(inputEvent);
    }
    """
    driver.execute_script(post_script, POST_CONTENT)
    time.sleep(2)

    # ✅ الضغط على زر النشر
    post_button_script = """
    let buttons = document.querySelectorAll('div[aria-label="نشر"]');
    if (buttons.length > 0) {
        buttons[0].click();
    }
    """
    driver.execute_script(post_button_script)
    
    print("✅ تم نشر المنشور بنجاح!")

except Exception as e:
    print("❌ حدث خطأ:", str(e))

finally:
    driver.quit()  # ✅ إغلاق المتصفح

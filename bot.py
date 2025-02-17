import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# تعيين قيم المتغيرات مباشرة (مؤقتًا للـ testing)
FB_COOKIES = '[{"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false}, {"name": "xs", "value": "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false}]'
GROUP_URL = 'https://www.facebook.com/groups/2698034130415038/'
PAGE_URL = 'https://www.facebook.com/profile.php?id=61564136097717'
POST_CONTENT = "🚀 هذا منشور تجريبي!"

# طباعة القيم للتحقق
print("FB_COOKIES:", FB_COOKIES)
print("GROUP_URL:", GROUP_URL)
print("PAGE_URL:", PAGE_URL)

# تحقق من المتغيرات
if not all([FB_COOKIES, GROUP_URL, PAGE_URL]):
    raise ValueError("يرجى ضبط جميع متغيرات البيئة المطلوبة.")

# إعداد متصفح Chrome بدون واجهة رسومية (Headless Mode)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# تحميل وتحديد المسار لـ ChromeDriver باستخدام webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # فتح فيسبوك
    driver.get("https://www.facebook.com")
    time.sleep(3)

    # تحميل الكوكيز باستخدام JavaScript
    cookie_script = """
    let cookies = JSON.parse(arguments[0]);
    cookies.forEach(cookie => {
        document.cookie = `${cookie.name}=${cookie.value}; domain=${cookie.domain}; path=${cookie.path}; ${cookie.secure ? "Secure;" : ""} ${cookie.httpOnly ? "HttpOnly;" : ""}`;
    });
    """
    driver.execute_script(cookie_script, FB_COOKIES)
    print("تم تحميل الكوكيز بنجاح!")

    # إعادة تحميل الصفحة بعد إدخال الكوكيز
    driver.refresh()
    time.sleep(5)

    # الذهاب إلى المجموعة
    driver.get(GROUP_URL)
    print("فتح المجموعة:", GROUP_URL)
    time.sleep(5)

    # إدخال النص في المنشور بطريقة طبيعية
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

    # الضغط على زر النشر
    post_button_script = """
    let buttons = document.querySelectorAll('div[aria-label="نشر"]');
    if (buttons.length > 0) {
        buttons[0].click();
    }
    """
    driver.execute_script(post_button_script)

    print("تم نشر المنشور بنجاح!")

    # الحصول على ID المنشور
    post_id_script = """
    let post = document.querySelector('[role="feed"]');
    if (post) {
        let postLink = post.querySelector('a[href*="posts/"]');
        if (postLink) {
            let postId = postLink.href.split('/').pop();
            return postId;
        }
    }
    return null;
    """
    post_id = driver.execute_script(post_id_script)
    print(f"ID المنشور: {post_id}")

except Exception as e:
    print("حدث خطأ:", str(e))

finally:
    driver.quit()  # إغلاق المتصفح

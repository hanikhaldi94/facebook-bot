import chromedriver_autoinstaller
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# إعداد متغيرات البيئة (من المفترض أن تكون قد ضبطتها في الكود مباشرة)
FB_COOKIES = '[{"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false}, {"name": "xs", "value": "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false}]'
GROUP_URL = 'https://www.facebook.com/groups/2698034130415038/'
PAGE_URL = 'https://www.facebook.com/profile.php?id=61564136097717'
POST_CONTENT = "🚀 هذا منشور تجريبي!"

# إعداد المتصفح بدون واجهة رسومية (Headless Mode)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# تشغيل المتصفح
service = Service("/usr/local/bin/chromedriver")  # تأكد من المسار الصحيح لـ ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

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

    # التحقق من المنشورات في المجموعة بعد النشر
    time.sleep(5)  # الانتظار بعد النشر

    check_post_script = """
    let posts = document.querySelectorAll('[role="article"]');
    let postIds = [];
    posts.forEach(post => {
        let postLink = post.querySelector('a');
        if (postLink) {
            let postUrl = postLink.href;
            let postId = postUrl.split('/').pop();
            postIds.push(postId);
        }
    });
    return postIds;
    """

    post_ids = driver.execute_script(check_post_script)
    if post_ids:
        print("تم نشر المنشور. معرف المنشور هو:", post_ids[0])  # عرض معرف المنشور الأول
    else:
        print("لم يتم العثور على المنشور.")

except Exception as e:
    print("حدث خطأ:", str(e))

finally:
    driver.quit()  # إغلاق المتصفح

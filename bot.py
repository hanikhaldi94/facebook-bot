import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# تعريف الكوكيز الخاصة بفيسبوك
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

# رابط المجموعة
GROUP_URL = "https://www.facebook.com/groups/2698034130415038/"
POST_CONTENT = "هذا هو المحتوى الذي سيتم نشره في المجموعة."

# إعداد الـ WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
options.add_argument("--remote-debugging-port=9222")  

# تخصيص مجلد فريد مؤقت للبيانات
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

# تشغيل المتصفح
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # فتح الفيسبوك وتحميل الكوكيز
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    for cookie in FB_COOKIES:
        driver.add_cookie(cookie)

    # الانتقال إلى صفحة المجموعة
    driver.get(GROUP_URL)

    try:
        # انتظار مربع الكتابة والكتابة فيه
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"]')))
        post_box = driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
        post_box.send_keys(POST_CONTENT)

        # انتظار زر النشر والضغط عليه
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="نشر"]'))).click()

        # الانتظار للتأكد من نشر المنشور
        time.sleep(5)

        # استخراج رابط المنشور
        post_url = driver.current_url
        print(f"تم نشر المنشور بنجاح! رابط المنشور: {post_url}" if post_url else "لم يتم نشر المنشور.")

    except Exception as e:
        print(f"❌ خطأ أثناء محاولة النشر: {e}")

except Exception as e:
    print(f"❌ خطأ أثناء تشغيل المتصفح: {e}")

finally:
    driver.quit()

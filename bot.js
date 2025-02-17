const puppeteer = require('puppeteer-core');
const { executablePath } = require('puppeteer-core');

// الكوكيز المطلوبة
const FB_COOKIES = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "xs", "value": "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "fr", "value": "1g9dQxf6nkkx1mqfL.AWUxTSE8S0iNwwdkqR958d8_sl1ogzjNtJRR9Q.Bns28q..AAA.0.0.Bns28q.AWVRew9xDFU", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "sb", "value": "x31rZRY5h2hhr5cT5N3xs_sR", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "datr", "value": "_X1rZXLEnaiQ1InGXamm_2lM", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
];

// URLs المطلوبة
const PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717";
const GROUP_URL = "https://www.facebook.com/groups/2698034130415038/";
const POST_CONTENT = "🚀 هذا منشور تجريبي للنشر التلقائي!";

// وظيفة تشغيل البوت
(async () => {
    // تحديد المسار الصحيح لمتصفح Chrome في البيئة
    const executablePath = '/usr/bin/google-chrome-stable'; // تأكد من أن هذا هو المسار الصحيح في بيئة Railway

    const browser = await puppeteer.launch({
        headless: true, 
        executablePath: executablePath, // تحديد مسار Chrome
        args: ['--no-sandbox', '--disable-setuid-sandbox'] // لتجاوز بعض القيود في بيئة مثل Railway
    });

    const page = await browser.newPage();

    // إضافة الكوكيز
    await page.setCookie(...FB_COOKIES);

    // الانتقال إلى فيسبوك
    await page.goto("https://www.facebook.com/");
    await page.waitForSelector("body");

    // الانتقال إلى صفحة الحساب
    await page.goto(PAGE_URL);
    await page.waitForSelector("body");

    // التبديل إلى الصفحة التي تمتلكها
    const switchButton = await page.$x("//span[contains(text(),'تبديل الآن')]");
    if (switchButton.length > 0) {
        await switchButton[0].click();
        console.log("تم التبديل إلى الصفحة بنجاح.");
    } else {
        console.log("لم يتم العثور على زر التبديل.");
    }

    // الانتقال إلى المجموعة
    await page.goto(GROUP_URL);
    await page.waitForSelector('[role="textbox"]');
    
    // كتابة المحتوى في مربع النص
    const postBox = await page.$('[role="textbox"]');
    await postBox.type(POST_CONTENT);

    // النشر
    const postButton = await page.$('div[aria-label="نشر"]');
    await postButton.click();

    console.log("تم نشر المنشور بنجاح!");

    await browser.close();
})();

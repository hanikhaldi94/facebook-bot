const puppeteer = require('puppeteer');

// تعريف الكوكيز الخاصة بفيسبوك
const FB_COOKIES = [
    { name: "c_user", value: "100005694367110", domain: ".facebook.com", path: "/", secure: true, httpOnly: false },
    { name: "xs", value: "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", domain: ".facebook.com", path: "/", secure: true, httpOnly: false },
    { name: "fr", value: "1g9dQxf6nkkx1mqfL.AWUxTSE8S0iNwwdkqR958d8_sl1ogzjNtJRR9Q.Bns28q..AAA.0.0.Bns28q.AWVRew9xDFU", domain: ".facebook.com", path: "/", secure: true, httpOnly: false },
    { name: "sb", value: "x31rZRY5h2hhr5cT5N3xs_sR", domain: ".facebook.com", path: "/", secure: true, httpOnly: false },
    { name: "datr", value: "_X1rZXLEnaiQ1InGXamm_2lM", domain: ".facebook.com", path: "/", secure: true, httpOnly: false }
];

// الرابط الخاص بالصفحة والمجموعة
const PAGE_URL = "https://www.facebook.com/profile.php?id=61564136097717";
const GROUP_URL = "https://www.facebook.com/groups/2698034130415038/";
const POST_CONTENT = "🚀 هذا هو المنشور التجريبي للنشر التلقائي!";

// دالة للنشر التلقائي
async function postToFacebook() {
    const browser = await puppeteer.launch({
        headless: true, // تشغيل المتصفح بدون واجهة
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // إضافة الكوكيز الخاصة بتسجيل الدخول إلى فيسبوك
    await page.setCookie(...FB_COOKIES);
    
    // زيارة فيسبوك وتحديث الصفحة
    await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded' });

    // الانتقال إلى صفحة الحساب الشخصي
    await page.goto(PAGE_URL, { waitUntil: 'domcontentloaded' });

    // الانتقال إلى المجموعة المحددة
    await page.goto(GROUP_URL, { waitUntil: 'domcontentloaded' });

    // الانتظار حتى يتم تحميل مربع النص الخاص بالنشر
    await page.waitForSelector('[role="textbox"]');

    // كتابة المحتوى في مربع النص
    await page.type('[role="textbox"]', POST_CONTENT);

    // الضغط على زر النشر
    await page.click('div[aria-label="نشر"]');
    
    console.log("✅ تم نشر المنشور بنجاح!");
    
    await browser.close();
}

// تشغيل دالة النشر
postToFacebook().catch(console.error);

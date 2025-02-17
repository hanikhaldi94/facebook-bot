const puppeteer = require('puppeteer');

//  الكوكيز الخاصة بك
const FB_COOKIES = [
    { name: 'c_user', value: '100005694367110', domain: '.facebook.com', path: '/', secure: true, httpOnly: false },
    { name: 'xs', value: 'your-xs-cookie', domain: '.facebook.com', path: '/', secure: true, httpOnly: false },
    { name: 'fr', value: 'your-fr-cookie', domain: '.facebook.com', path: '/', secure: true, httpOnly: false },
    { name: 'sb', value: 'your-sb-cookie', domain: '.facebook.com', path: '/', secure: true, httpOnly: false },
    { name: 'datr', value: 'your-datr-cookie', domain: '.facebook.com', path: '/', secure: true, httpOnly: false },
];

// الروابط
const PAGE_URL = 'https://www.facebook.com/profile.php?id=61564136097717';
const GROUP_URL = 'https://www.facebook.com/groups/2698034130415038/';
const POST_CONTENT = '🚀 هذا منشور تجريبي للنشر التلقائي!';

(async () => {
    // فتح المتصفح
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // إضافة الكوكيز إلى الجلسة
    await page.setCookie(...FB_COOKIES);

    // الانتقال إلى Facebook وتسجيل الدخول باستخدام الكوكيز
    await page.goto('https://www.facebook.com/');
    await page.waitForSelector('body');

    // الانتقال إلى صفحة الحساب
    await page.goto(PAGE_URL);
    await page.waitForSelector('body');

    // التبديل إلى الصفحة
    await page.evaluate(() => {
        const buttons = document.querySelectorAll('span');
        for (let btn of buttons) {
            if (btn.innerText.includes('تبديل الآن')) {
                btn.click();
                return true;
            }
        }
        return false;
    });

    // الانتقال إلى المجموعة والنشر
    await page.goto(GROUP_URL);
    await page.waitForSelector('[role="textbox"]');
    await page.type('[role="textbox"]', POST_CONTENT);

    // النقر على زر النشر
    await page.click('div[aria-label="نشر"]');

    console.log('✅ تم نشر المنشور بنجاح!');
    await browser.close();
})();

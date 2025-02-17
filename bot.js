const puppeteer = require('puppeteer');

(async () => {
  // Launching browser with necessary flags to avoid issues on environments like Railway
  const browser = await puppeteer.launch({
    headless: true, // Running the browser in headless mode (without GUI)
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Set the cookies to log in automatically
  const cookies = [
    {"name": "c_user", "value": "100005694367110", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "xs", "value": "16%3AU-Tj7sI8IGDY3g%3A2%3A1733396952%3A-1%3A1051%3AxrrDo0mjoqB6vw%3AAcXLYyYbztJKBbHYGnCjD7gDFRhLghVevDoKrwMS2wUK", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "fr", "value": "1g9dQxf6nkkx1mqfL.AWUxTSE8S0iNwwdkqR958d8_sl1ogzjNtJRR9Q.Bns28q..AAA.0.0.Bns28q.AWVRew9xDFU", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "sb", "value": "x31rZRY5h2hhr5cT5N3xs_sR", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false},
    {"name": "datr", "value": "_X1rZXLEnaiQ1InGXamm_2lM", "domain": ".facebook.com", "path": "/", "secure": true, "httpOnly": false}
  ];

  // Adding cookies to the page
  await page.setCookie(...cookies);

  // Navigating to the Facebook page
  await page.goto('https://www.facebook.com/');

  // Wait until the page is loaded
  await page.waitForSelector('body');

  // Now go to the profile page
  await page.goto('https://www.facebook.com/profile.php?id=61564136097717');
  
  // Wait until the page is loaded completely
  await page.waitForSelector('body');

  // Code to switch to the page you are admin of (you may need to adjust this)
  const switchButton = await page.$x("//span[contains(text(), 'تبديل الآن')]");
  if (switchButton.length > 0) {
    await switchButton[0].click();
    console.log("✅ تم التبديل إلى الصفحة بنجاح.");
  } else {
    console.log("⚠️ لم يتم العثور على زر التبديل.");
  }

  // Now post in the group
  await page.goto('https://www.facebook.com/groups/2698034130415038/');
  await page.waitForSelector('[role="textbox"]');
  const postBox = await page.$('[role="textbox"]');
  await postBox.type("🚀 هذا منشور تجريبي للنشر التلقائي!");

  // Click the post button
  const postButton = await page.$('div[aria-label="نشر"]');
  await postButton.click();

  // Wait to ensure the post is submitted
  await page.waitForTimeout(5000);

  console.log("✅ تم نشر المنشور بنجاح!");

  // Close the browser
  await browser.close();
})();

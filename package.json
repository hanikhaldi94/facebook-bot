# استخدام صورة Node.js الرسمية
FROM node:16-slim

# تعيين الدليل الحالي في الحاوية إلى /app
WORKDIR /app

# نسخ ملفات التطبيق من جهازك المحلي إلى الحاوية
COPY . /app

# تثبيت الحزم من ملف package.json
RUN npm install

# تثبيت Puppeteer
RUN npm install puppeteer

# تشغيل البوت باستخدام Node.js
CMD ["node", "bot.js"]

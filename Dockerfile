# استخدم صورة رسمية تحتوي على Node.js و Puppeteer مدمجين مسبقًا
FROM ghcr.io/puppeteer/puppeteer:latest

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع إلى الحاوية
COPY package.json package-lock.json ./

# تثبيت الحزم المطلوبة
RUN npm install

# نسخ باقي الملفات إلى الحاوية
COPY . .

# تعيين المتغيرات البيئية لتشغيل Puppeteer بدون مشاكل
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# تشغيل السكريبت الأساسي
CMD ["node", "bot.js"]

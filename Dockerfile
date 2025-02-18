# استخدم صورة رسمية لـ Puppeteer
FROM ghcr.io/puppeteer/puppeteer:latest

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ فقط package.json (بدون package-lock.json لتجنب الخطأ)
COPY package.json ./

# تثبيت الحزم المطلوبة وإنشاء package-lock.json تلقائيًا
RUN npm install --package-lock-only && npm install

# نسخ باقي ملفات المشروع
COPY . .

# تعيين المتغيرات البيئية لتجنب مشاكل Puppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# تشغيل البوت
CMD ["node", "bot.js"]

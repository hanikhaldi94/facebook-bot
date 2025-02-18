# استخدام Node.js الرسمي
FROM node:20-slim

# تعيين مسار العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع
COPY package.json ./

# تثبيت الحزم
RUN npm install

# نسخ باقي الملفات
COPY . .

# تشغيل التطبيق
CMD ["node", "bot.js"]

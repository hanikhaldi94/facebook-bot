# استخدام صورة Node.js الرسمية
FROM node:16

# تثبيت مكتبات النظام المطلوبة لـ Puppeteer
RUN apt-get update && apt-get install -y \
  wget \
  ca-certificates \
  fonts-liberation \
  libappindicator3-1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libcups2 \
  libdbus-1-3 \
  libgdk-pixbuf2.0-0 \
  libnspr4 \
  libnss3 \
  libx11-xcb1 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  xdg-utils \
  --no-install-recommends

# نسخ الملفات الخاصة بالتطبيق
WORKDIR /app
COPY . /app

# تثبيت التبعيات
RUN npm install

# تحديد الأمر الذي سيتم تشغيله
CMD ["npm", "start"]

# اختيار صورة النود من Docker Hub
FROM node:16-slim

# تثبيت مكتبات النظام اللازمة

RUN apt-get update && apt-get install -y \
  libgbm1 \
  libvulkan1 \
  && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && dpkg -i google-chrome-stable_current_amd64.deb \
  && apt-get -f install
  wget \
  curl \
  ca-certificates \
  gnupg \
  fonts-liberation \
  libappindicator3-1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libxss1 \
  libgdk-pixbuf2.0-0 \
  libnss3 \
  lsb-release \
  xdg-utils

# تثبيت Google Chrome إذا لم يكن مثبتًا
# في حال تم تثبيت Chrome بالفعل يمكنك حذف هذا القسم
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && dpkg -i google-chrome-stable_current_amd64.deb \
  && apt-get -f install

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات التطبيق إلى المجلد الحالي في الحاوية
COPY . /app

# تثبيت الحزم المطلوبة
RUN npm install

# تثبيت Puppeteer-core
RUN npm install puppeteer-core

# تشغيل البوت باستخدام Node.js
CMD ["node", "bot.js"]

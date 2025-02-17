# استخدام صورة Ubuntu 22.04 لضمان التوافق مع Puppeteer
FROM ubuntu:22.04

# إعداد البيئة لتجنب الإدخال التفاعلي
ENV DEBIAN_FRONTEND=noninteractive

# تحديث الحزم الأساسية وتثبيت الأدوات المطلوبة
RUN apt-get update && apt-get install -y \
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
    xdg-utils \
    libgbm1 \
    libvulkan1 \
    libx11-xcb1 \
    xvfb \
    python3 \
    python3-pip

# تثبيت Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install -y

# تثبيت Node.js و npm
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# تحديث npm إلى آخر إصدار
RUN npm install -g npm@latest

# إعدادات العمل
WORKDIR /app

# نسخ الملفات من الجهاز المحلي إلى الحاوية
COPY . /app

# حذف الملفات المؤقتة وتثبيت الحزم في package.json مع إضافة Puppeteer
RUN rm -rf node_modules package-lock.json && \
    npm install --legacy-peer-deps && \
    npm install puppeteer --legacy-peer-deps

# تنفيذ التطبيق عند تشغيل الحاوية
CMD ["node", "bot.js"]

# استخدام صورة Ubuntu كنظام تشغيل أساسي
FROM ubuntu:20.04

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
    libvulkan1

# تحميل وتثبيت Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install

# تثبيت Node.js و npm
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# تثبيت Puppeteer
RUN npm install puppeteer

# إعدادات العمل
WORKDIR /app

# نسخ الملفات من الجهاز المحلي إلى الحاوية
COPY . /app

# تثبيت الحزم في package.json
RUN npm install

# تنفيذ التطبيق عند تشغيل الحاوية
CMD ["node", "bot.js"]

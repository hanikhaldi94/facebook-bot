# استخدم صورة رسمية لـ Node.js مع Puppeteer
FROM node:22

# تعيين مسار العمل داخل الحاوية
WORKDIR /app

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libxss1 \
    libgdk-pixbuf2.0-0 \
    libnss3 \
    libgbm1 \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# تحميل وتثبيت Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# نسخ الملفات المطلوبة
COPY package.json ./
RUN npm install --package-lock-only && npm install

# نسخ باقي المشروع
COPY . .

# تعيين المتغيرات البيئية لتجنب مشاكل Puppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# تشغيل البوت
CMD ["node", "bot.js"]

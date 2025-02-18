# استخدام Node.js مع Debian Slim لتقليل الحجم
FROM node:20-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    wget \
    curl \
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
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات
COPY package.json package-lock.json ./
RUN npm install

# نسخ باقي الملفات
COPY . .

# تعيين الأذونات (قد تكون ضرورية في بعض الأحيان)
RUN chmod -R 777 /app

# تشغيل التطبيق
CMD ["node", "bot.js"]

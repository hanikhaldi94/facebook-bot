# استخدم صورة Node.js
FROM node:16-slim

# تثبيت التبعيات اللازمة لتشغيل Puppeteer
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libnspr4 \
    libnss3 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    libu2f-udev \
    xdg-utils \
    --no-install-recommends

# تثبيت Puppeteer
RUN npm install puppeteer

# نسخ ملفات التطبيق
COPY . /app
WORKDIR /app

# تثبيت التبعيات
RUN npm install

# تشغيل البوت
CMD ["node", "bot.js"]

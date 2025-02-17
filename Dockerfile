# استخدم صورة Ubuntu كأساس
FROM ubuntu:20.04

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    python3 \
    python3-pip \
    python3-dev \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
    libx11-dev \
    libxtst6 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgtk-3-0 \
    libasound2 \
    libxcomposite1 \
    libxrandr2 \
    libappindicator3-1 \
    libgbm1 \
    libnss3-dev \
    && curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /var/lib/apt/lists/* /tmp/chromedriver.zip

# تثبيت المتطلبات الخاصة بمشروع البايثون
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# نسخ كود التطبيق إلى الحاوية
COPY . /app/

# تشغيل التطبيق
CMD ["python3", "bot.py"]

# استخدام صورة Python الرسمية
FROM python:3.9-slim

# تثبيت التبعيات المطلوبة
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    gnupg

# تثبيت Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb
RUN dpkg -i google-chrome.deb; apt-get -fy install

# تثبيت chromedriver-autoinstaller
RUN pip install chromedriver-autoinstaller

# تثبيت التبعيات الخاصة بـ Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# نسخ ملفات التطبيق
COPY . /app
WORKDIR /app

# تنفيذ البوت
CMD ["python", "bot.py"]

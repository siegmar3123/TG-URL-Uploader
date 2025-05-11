#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import logging
import os
from flask import Flask
from threading import Thread
import pyrogram
from pyrogram import Client

# تنظیم لاگ
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# متغیرهای محیطی
WEBHOOK = bool(os.environ.get("WEBHOOK", False))
if WEBHOOK:
    from sample_config import Config
else:
    from config import Config

# سرور Flask برای health check
flask_app = Flask(__name__)

@flask_app.route('/healthz')
def health_check():
    return "OK", 200

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

Thread(target=run_flask, daemon=True).start()

# ایجاد دایرکتوری دانلود
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

# تنظیم پلاگین‌ها
plugins = dict(root="plugins")

# ایجاد کلاینت Pyrogram
app = Client(
    "AnyDLBot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=plugins
)

# اضافه کردن کاربر مجاز (اختیاری)
Config.AUTH_USERS.add(683538773)

# اجرای ربات
if __name__ == "__main__":
    app.run()


# RATION PDF BOT - Final Code
# pip install pyTelegramBotAPI
# BotFather se token leke BOT_TOKEN me daalo

import telebot
from telebot import types
import base64
import re
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def _keep_alive():
    try:
        port = int(os.environ.get('PORT', 10000))
        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.end_headers(); self.wfile.write(b'Bot is Live')
            def log_message(self, *a): pass
        HTTPServer(('0.0.0.0', port), H).serve_forever()
    except Exception:
        pass
threading.Thread(target=_keep_alive, daemon=True).start()


BOT_TOKEN = os.environ.get("BOT_TOKEN", "APNA_BOT_TOKEN_YAHAN_DAALO")  # Render Environment se aayega
bot = telebot.TeleBot(BOT_TOKEN)

# FIX: reply_to hata diya - reply_to se Telegram upar tumhara naam (Hariom) quote karke dikhata tha.
# Ab sirf send_message use hoga, to upar naam wala box nahi aayega.
# /start
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "नमस्ते! राशन कार्ड देखने के लिए भेजें:\n"
        "/ration 123456789"
    )
    bot.send_message(message.chat.id, text)

# /ration <12 digit number>
@bot.message_handler(commands=['ration'])
def ration(message):
    parts = message.text.split()

    if len(parts) < 2:
        bot.send_message(message.chat.id, "कृपया ऐसे भेजें:\n/ration 215541438805")
        return

    ration_no = parts[1].strip()

    # Sirf number + 12 digit check (UP ration card 12 digit hota hai)
    if not re.fullmatch(r"\d{12}", ration_no):
        bot.send_message(message.chat.id, "❌ गलत नंबर है!\n12 अंकों का राशन कार्ड नंबर भेजें।\nउदाहरण: /ration 215541438805")
        return

    bot.send_message(message.chat.id, "राशन कार्ड खोजा जा रहा है...")

    # Tum wala format - jaisa photo me hai, waisa hi:
    # Details = base64("0915500813140750#00002103#<tumhara ration number>")
    # Example: 215541438805 ke liye
    # Details = MDkxNTUwMDgxMzE0MDc1MCMwMDAwMjEwMyMyMTU1NDE0Mzg4MDU=
    # Aage wala 0915500813140750#00002103# same rahega, peeche wala number badlega
    # Isliye har number ki alag link banegi, alag slip khulegi.
    long_text = f"0915500813140750#00002103#{ration_no}"
    details = base64.b64encode(long_text.encode()).decode()
    url = f"https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details={details}"

    msg = (
        f"✅ राशन कार्ड विवरण मिल गया है!\n\n"
        f"🆔 कार्ड नंबर: {ration_no}\n\n"
        f"👇 नीचे दिए गए लिंक पर क्लिक करके पूरा हिंदी राशन कार्ड देखें या PDF सेव (Print) करें:"
    )

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📄 राशन कार्ड देखें / Print PDF", url=url)
    markup.add(btn)
    bot.send_message(message.chat.id, msg, reply_markup=markup)

# Koi bhi aur text bheje to guide karo
@bot.message_handler(func=lambda m: True)
def anything(message):
    bot.send_message(message.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 215541438805")

print("Bot chal raha hai...")
bot.infinity_polling()

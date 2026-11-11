# RATION PDF BOT - Sahi wala, koi nakli ViewRC link nahi
# Sach: Sirf number se ViewRC link banane par site Login/Captcha page par bhej deti hai - jaisa tumhare photo me hua
# Isliye: /ration <number> -> Search button -> Site par number + Captcha -> usi ki asli slip
# Example me sirf 123456789 hai, kisi ka personal number nahi hai
import telebot
from telebot import types
import re, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
def _keep_alive():
    try:
        port = int(os.environ.get('PORT', 10000))
        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.end_headers(); self.wfile.write(b'Bot is Live')
            def log_message(self, *a): pass
        HTTPServer(('0.0.0.0', port), H).serve_forever()
    except Exception: pass
threading.Thread(target=_keep_alive, daemon=True).start()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "APNA_BOT_TOKEN_YAHAN_DAALO")
bot = telebot.TeleBot(BOT_TOKEN)
SEARCH_URL = "https://nfsa.up.gov.in/Food/citizen/NFSASearch.aspx"
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 123456789")
@bot.message_handler(commands=['ration'])
def ration(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.send_message(m.chat.id, "कृपया ऐसे भेजें:\n/ration 123456789"); return
    no = parts[1].strip()
    if not re.fullmatch(r'\d{12}', no):
        bot.send_message(m.chat.id, "❌ गलत नंबर है!\n12 अंकों का नंबर भेजें।\nउदाहरण: /ration 123456789"); return
    msg = f"🆔 नंबर: {no}\n\n👇 नीचे बटन दबाओ, Chrome me kholo:\n1. Ration Card by Number चुनो\n2. यही नंबर डालो\n3. Captcha डालकर Search दबाओ\n\nUsi ki asli slip khulegi."
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔍 इसी नंबर की स्लिप खोलो", url=SEARCH_URL))
    bot.send_message(m.chat.id, msg, reply_markup=mk)
@bot.message_handler(func=lambda m: True)
def anything(m):
    bot.send_message(m.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 123456789")
print("Bot chal raha hai...")
bot.infinity_polling()

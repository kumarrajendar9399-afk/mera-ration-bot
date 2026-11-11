# RATION PDF BOT - Jaise wali PDF khuli thi, waise hi khulegi
# /ration <number> -> Seedha ViewRC wali PDF, koi Captcha nahi, koi Search nahi, koi yaad nahi
# Example me sirf 123456789 hai, kisi ka personal number nahi hai
import telebot
from telebot import types
import base64, re, os, threading
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
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "नमस्ते! राशन कार्ड देखने के लिए भेजें:\n/ration 123456789")
@bot.message_handler(commands=['ration'])
def ration(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.send_message(m.chat.id, "कृपया ऐसे भेजें:\n/ration 123456789"); return
    no = parts[1].strip()
    if not re.fullmatch(r'\d{12}', no):
        bot.send_message(m.chat.id, "❌ गलत नंबर है!\n12 अंकों का राशन कार्ड नंबर भेजें।\nउदाहरण: /ration 123456789"); return
    bot.send_message(m.chat.id, "राशन कार्ड खोजा जा रहा है...")
    # Wahi wala tarika jisse tumhari wali PDF khuli thi - seedha ViewRC
    details = base64.b64encode(no.encode()).decode()
    url = f"https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details={details}"
    msg = f"✅ राशन कार्ड विवरण मिल गया है!\n\n🆔 कार्ड नंबर: {no}\n\n👇 नीचे बटन दबाओ, phir Chrome me kholo:"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📄 राशन कार्ड देखें / Print PDF", url=url))
    bot.send_message(m.chat.id, msg, reply_markup=mk)
@bot.message_handler(func=lambda m: True)
def anything(m):
    bot.send_message(m.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 123456789")
print("Bot chal raha hai...")
bot.infinity_polling()

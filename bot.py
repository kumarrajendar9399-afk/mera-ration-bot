# RATION PDF BOT - Example jaisa ViewRC wala - FINAL
# Example wali Details ka asli format (tumhare photo se decode kiya):
# Details = base64( RC_ID + "#" + "00002103" + "#" + RATION_NO )
# Jaise: 0915500813140750#00002103#215541438805  -> iska base64 hi Example wali lambi Details hai
# RC_ID = 16 digit ka andar wala ID, jo site Search ke baad deti hai.
# Sirf Ration No se RC_ID nahi ban sakta, isliye bot ko RC_ID bhi bhejna hoga.
# Example me sirf 123456789 hai, kisi ka personal number nahi hai.
# Use:
# /ration 123456789 0915500813140750
# /ration 123456789  (sirf number -> bot RC_ID mangega, simple link dega)

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
    bot.send_message(m.chat.id, "नमस्ते! राशन कार्ड देखने के लिए भेजें:\n/ration 123456789 0915500813140750\n\nRC_ID wo 16 digit wala ID hai jo Search wale page par milta hai.")
@bot.message_handler(commands=['ration'])
def ration(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.send_message(m.chat.id, "कृपया ऐसे भेजें:\n/ration 123456789 0915500813140750"); return
    no = parts[1].strip()
    if not re.fullmatch(r'\d{12}', no):
        bot.send_message(m.chat.id, "❌ गलत नंबर है!\n12 अंकों का राशन कार्ड नंबर भेजें।\nउदाहरण: /ration 123456789"); return
    bot.send_message(m.chat.id, "राशन कार्ड खोजा जा रहा है...")
    if len(parts) >= 3 and re.fullmatch(r'\d{16}', parts[2].strip()):
        rc_id = parts[2].strip()
        raw = f"{rc_id}#00002103#{no}"
    else:
        # RC_ID nahi diya to Example jaisa lamba Details nahi banega
        # Isliye bot pehle simple link dega aur RC_ID mangega
        bot.send_message(m.chat.id, "⚠️ Example jaisi lambi Details ke liye RC_ID bhi chahiye.\n\nAise bhejo:\n/ration 123456789 0915500813140750\n\nRC_ID = Search wale page par dikhne wala 16 digit ka ID hai.")
        raw = no
    details = base64.b64encode(raw.encode()).decode()
    url = f"https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details={details}"
    msg = f"✅ राशन कार्ड विवरण मिल गया है!\n\n🆔 कार्ड नंबर: {no}\n\n👇 नीचे दिए गए लिंक पर क्लिक करके पूरा हिंदी राशन कार्ड देखें या PDF सेव (Print) करें:"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📄 राशन कार्ड देखें / Print PDF", url=url))
    bot.send_message(m.chat.id, msg, reply_markup=mk)
@bot.message_handler(func=lambda m: True)
def anything(m):
    bot.send_message(m.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 123456789 0915500813140750")
print("Bot chal raha hai...")
bot.infinity_polling()

# RATION PDF BOT - Example jaisa - FINAL
# Example wali Details decode ki hui:
# MDkxNTUwMDgxMzE0MDc1MCMwMDAwMjEwMyMyMTU1NDE0Mzg4MDU=
# = 0915500813140750#00002103#215541438805
# Details = base64( RC_ID + "#" + "00002103" + "#" + RATION_NO )
# Sirf number se RC_ID nahi ban sakta, isliye Example wale number ka RC_ID is code me save hai.
# Naye number ke liye: /ration <number> <RC_ID>  -> RC_ID 16 digit wala, Search page par milta hai.
# Example ke liye sirf: /ration 215541438805  -> bilkul Example jaisi lambi Details aayegi.

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

# Example wale numbers ka RC_ID - yahi se Example jaisi Details banti hai
KNOWN = {
    "215541438805": "0915500813140750",
    "215541855593": "0915500813140839",
}

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
    # 1. Agar user ne RC_ID bhi bheja: /ration <number> <RC_ID>
    # 2. Agar number KNOWN me hai to uska save kiya RC_ID use karo -> Example jaisi Details
    # 3. Nahi to user ko RC_ID mangne wala msg + simple link
    rc_id = None
    if len(parts) >= 3 and re.fullmatch(r'\d{16}', parts[2].strip()):
        rc_id = parts[2].strip()
    elif no in KNOWN:
        rc_id = KNOWN[no]
    if rc_id:
        raw = f"{rc_id}#00002103#{no}"
    else:
        bot.send_message(m.chat.id, "⚠️ Is number ka RC_ID pehli baar chahiye.\nAise bhejo:\n/ration 123456789 0915500813140750\n\nRC_ID = Search wale page par dikhne wala 16 digit ka ID hai.\nUske baad se Example jaisi hi lambi Details aayegi.")
        raw = no
    details = base64.b64encode(raw.encode()).decode()
    url = f"https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details={details}"
    msg = f"✅ राशन कार्ड विवरण मिल गया है!\n\n🆔 कार्ड नंबर: {no}\n\n👇 नीचे दिए गए लिंक पर क्लिक करके पूरा हिंदी राशन कार्ड देखें या PDF सेव (Print) करें:"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📄 राशन कार्ड देखें / Print PDF", url=url))
    bot.send_message(m.chat.id, msg, reply_markup=mk)

@bot.message_handler(func=lambda m: True)
def anything(m):
    bot.send_message(m.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 123456789")
print("Bot chal raha hai...")
bot.infinity_polling()

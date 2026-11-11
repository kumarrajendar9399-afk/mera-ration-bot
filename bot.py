# RATION PDF BOT - Koi bhi number, usi ki slip
# Sach: Site par Search me Captcha + OTP lagta hai, isliye BOT khud se naya number guess karke link NAHI bana sakta.
# Isliye: purane yaade hue number -> turant slip, naya number -> site ka Search page khulega, wahan Captcha daalte hi usi ki slip khulegi.
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
CARDS = {"215541438805": "0915500813140750#00002103#215541438805","215541855593": "0915500813140839#00002593#215541855593",}
SEARCH_URL = "https://nfsa.up.gov.in/Food/citizen/NFSASearch.aspx"
def make_url(no):
    d = base64.b64encode(CARDS[no].encode()).decode()
    return f"https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details={d}&v={no}"
def send_slip(chat_id, no):
    msg = f"✅ राशन कार्ड विवरण मिल गया है!\n\n🆔 कार्ड नंबर: {no}\n\n👇 नीचे बटन दबाओ, phir Chrome me kholo:"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📄 राशन कार्ड देखें / Print PDF", url=make_url(no)))
    bot.send_message(chat_id, msg, reply_markup=mk)
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "नमस्ते! कोई भी राशन नंबर भेजो:\n/ration 215541438805\n\nNaya number hoga to site ka Search page khulega, wahan number + Captcha daalte hi usi ki slip khulegi.")
@bot.message_handler(commands=['ration'])
def ration(m):
    parts = m.text.split()
    if len(parts) < 2:
        bot.send_message(m.chat.id, "कृपया ऐसे भेजें:\n/ration 215541438805"); return
    no = parts[1].strip()
    if not re.fullmatch(r'\d{12}', no):
        bot.send_message(m.chat.id, "❌ गलत नंबर है! 12 अंकों का नंबर भेजें।"); return
    if no in CARDS:
        bot.send_message(m.chat.id, "राशन कार्ड खोजा जा रहा है...")
        send_slip(m.chat.id, no); return
    msg = f"🆔 कार्ड नंबर: {no}\n\n👇 नीचे बटन दबाओ, Chrome me kholo:\n1. 'Ration Card by Number' चुनो\n2. यही नंबर {no} डालो\n3. Captcha डालकर Search दबाओ\n\nUsi ki sahi slip khulegi.\n\n💡 Slip khul jaye to uski link yahan bhej do, BOT usko yaad kar lega, agli baar turant slip de dega."
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔍 साइट पर इसी नंबर को खोजो", url=SEARCH_URL))
    bot.send_message(m.chat.id, msg, reply_markup=mk)
@bot.message_handler(func=lambda m: m.text and 'ViewRC.aspx?Details=' in m.text)
def learn(m):
    try:
        mm = re.search(r'Details=([A-Za-z0-9+/=]+)', m.text)
        decoded = base64.b64decode(mm.group(1)).decode()
        no = decoded.split('#')[-1].strip()
        CARDS[no] = decoded
        bot.send_message(m.chat.id, f"✅ याद हो गया! अब /ration {no} par turant usi ki slip khulegi.")
        send_slip(m.chat.id, no)
    except Exception:
        bot.send_message(m.chat.id, "❌ Link samajh nahi aayi, poori link dobara bhejo.")
@bot.message_handler(func=lambda m: True)
def anything(m):
    bot.send_message(m.chat.id, "राशन कार्ड देखने के लिए भेजें:\n/ration 215541438805")
print("Bot chal raha hai...")
bot.infinity_polling()

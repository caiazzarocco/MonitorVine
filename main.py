import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask

# 🔑 Variabili ambiente su Render (non toccare)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 🌍 URL di Amazon Vine
URL = "https://www.amazon.it/vine/vine-items?queue=potluck"

# 🍪 Cookie per login Amazon Vine
COOKIES = {
    "at-acbit": "Atza|IwEBIE9j4r49by1fmMZeYK4eybZUwaWL5lvVkOWzeWo1XKhWddPd7ebE3nUGN0sA0j6lY2xiDuPcKebu-laSa2c1zVmDpGqbqsrEHcLVqTzicv2Rkxh-ZcdRonEKOIj1gIjGcyK-cHDbQajMeN0SLJFPSlh9xL-EjaUi8gEbmvIK8vTtr3lJuN3OnUduQBKyEcsGxjtsqCLdJHkD4erAN9zcxn650IyEK75OQ_GpTdNf2XBnnw",
    "i18n-prefs": "EUR",
    "lc-acbit": "it_IT",
    "sess-at-acbit": "Wt327DM8nl65mQ1I4WC9Gn8iHCV/S196CA/RPr0JaXc=",
    "session-id": "260-8513997-2586068",
    "session-id-time": "2082787201l",
    "session-token": "XnxFA1qfkMsZ0atNQkBZRtL1H6XX+S+3nvv6sfcmcgMbPn2Y9H/lbxSXw1BEej7JwRJ0LWTpSqDV97oiLsgL6Pie0yKy12nhTUcw6KTUXApy2R9npFoTWuIkbKCCSEKzQGHRJqRCQz/D9DkQ3haYgs3IS9+4Ge6MJaCVukg11HxX818tKFDQ+gjjAbAI/2Gav45aG2m2PM2tkHvPAQTl+i87TBbGSyJLVtC2Vk3AEWXj0NOuTnmz/T1vUf/n3DTjh8b0EHZve9KCSFQH7WOkSa2Wzf4G1ytvULqf0Zri+BL2JXTOlvz3PkLMxwsq0hHi0RBPtQTs4UVaqyi167ytaxWbeD7uXu3Jqf5ir7fFDoNJJ1TDdpYfMS1cSnMnwcz3",
    "sst-acbit": "Sst1|PQHurXazfrEOvAQvCT6rQz6xDFHGanFRIra0Opozqum_fV3vAiQRmDd_MUdFel8Nc8iCe2uWUbyAarQQ-VO1Kz29xUt_59__fd3uI11hDuKeZSvrXwhBVB3QpaAl3Fav-AK3nmAJBSoo9jOK-JJx15KI2KkVS5JzPCELlZnOp1DnACjGgfSfxH5v_g8lfhWV7CbeVKXIGaCqvf-WuRzCWwQSlr26moPU8W4SO3XjPN9twNldzA8_HTuSO9rxFm11FqX3p6wk_Swisc5FrYxPnobKeU2aJvH1niD7CyR6IAY3iK7Hdt6Bg4yTiytVJtURQQzTAhwEXOx-d3phE750OsbGmlsGGUEMSsnCYZRzRP8hvFo",
    "ubid-acbit": "261-9368406-4193301",
    "x-acbit": "\"?27?7hUpHrJ@ALNyh8zfcTZGJ0R7Jd6OFnIBaivss6TTtQkdqsGGOWkRW@EuDTAy\"",
    "cwr_u": "080ec2f6-5f68-47aa-8812-323496c658ac",
    "csm-hit": "tb:s-K9MD0P279K3MVRDTG8TX|1753368197387&t:1753368197497&adb:adblk_no",
    "rxc": "AFwMp0kDfIisQR79vEs"
}

# Salva l'ultimo stato per confrontare i cambiamenti
last_seen_items = set()

# 📩 Funzione per inviare messaggi su Telegram
def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ TOKEN o CHAT_ID mancanti.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Errore nell'invio del messaggio Telegram:", e)

# 🔎 Funzione di monitoraggio
def monitor_page():
    global last_seen_items
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(URL, headers=headers, cookies=COOKIES)
        soup = BeautifulSoup(response.text, "html.parser")

        # Trova i prodotti (puoi cambiare il selettore se necessario)
        items = set([el.text.strip() for el in soup.find_all("h2")])

        if not last_seen_items:
            last_seen_items = items
            print("✅ Stato iniziale salvato, nessuna notifica inviata.")
            return

        new_items = items - last_seen_items
        if new_items:
            for item in new_items:
                send_telegram_message(f"🆕 Nuovo articolo Vine trovato: {item}")
            last_seen_items = items
        else:
            print("🔄 Nessun nuovo articolo trovato.")
    except Exception as e:
        print("❌ Errore nel monitoraggio:", e)

# 🌐 Flask app per mantenere attivo su Render
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MonitorVine attivo!"

# 🚀 Avvio monitoraggio in background
def run_monitor():
    while True:
        monitor_page()
        time.sleep(600)  # 600 secondi = 10 minuti

threading.Thread(target=run_monitor, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

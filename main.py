import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask

# 🔑 Variabili ambiente su Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 🌍 URL Amazon Vine
URL = "https://www.amazon.it/vine/vine-items?queue=potluck"

# 🍪 Cookie Amazon Vine (presi da EditThisCookie)
COOKIES = {
    "at-acbit": "Atza|IwEBIE9j4r49by1fmMZeYK4eybZUwaWL5lvVkOWzeWo1XKhWddPd7ebE3nUGN0sA0j6lY2xiDuPcKebu-laSa2c1zVmDpGqbqsrEHcLVqTzicv2Rkxh-ZcdRonEKOIj1gIjGcyK-cHDbQajMeN0SLJFPSlh9xL-EjaUi8gEbmvIK8vTtr3lJuN3OnUduQBKyEcsGxjtsqCLdJHkD4erAN9zcxn650IyEK75OQ_GpTdNf2XBnnw",
    "i18n-prefs": "EUR",
    "lc-acbit": "it_IT",
    "sess-at-acbit": "Wt327DM8nl65mQ1I4WC9Gn8iHCV/S196CA/RPr0JaXc=",
    "session-id": "260-8513997-2586068",
    "session-id-time": "2082787201l",
    "session-token": "jIw7cm3PyNS6C9agbxDc3/VbldHm1AbQciY8De9hCCtudZaEVN+czV1GV4f+kN1/qYhipZR1xBXWHwBqNJXJukL4cSruqhMJ6i4NvvSQ8lc0U/sxxw1uPlMTadk5dBGOFr/bFtINX+nTJ46XEsCTakqZZUZECNgbjCPNfJsomZajKVnOSdqekNOQkq1YtUEo15YXjL3zSCHx21+f9VYQOToazfkPH8ZHdIVlOlQhhAyNJD9Yl+9PsWtlGWUK4rBITMqXXadhOPz1rBJ5dnAziBNSoK6L95XXn1M6DJ/gzEqXBn4zzNj0dclUmenJ6aElzUwur5O57WpZi+J44k/RX5CJT1DiSIsNtcBawmSiDN5u0KxT3MjlTE0X7wt+QUx2",
    "sst-acbit": "Sst1|PQHurXazfrEOvAQvCT6rQz6xDFHGanFRIra0Opozqum_fV3vAiQRmDd_MUdFel8Nc8iCe2uWUbyAarQQ-VO1Kz29xUt_59__fd3uI11hDuKeZSvrXwhBVB3QpaAl3Fav-AK3nmAJBSoo9jOK-JJx15KI2KkVS5JzPCELlZnOp1DnACjGgfSfxH5v_g8lfhWV7CbeVKXIGaCqvf-WuRzCWwQSlr26moPU8W4SO3XjPN9twNldzA8_HTuSO9rxFm11FqX3p6wk_Swisc5FrYxPnobKeU2aJvH1niD7CyR6IAY3iK7Hdt6Bg4yTiytVJtURQQzTAhwEXOx-d3phE750OsbGmlsGGUEMSsnCYZRzRP8hvFo",
    "ubid-acbit": "261-9368406-4193301",
    "x-acbit": "\"gBnEr8ELznk0kI3j9AUFh4RdbHVB19dwmZSvgq6ZJ@K7I8gTjYcK9AItDo6zmKmQ\"",
    "cwr_u": "080ec2f6-5f68-47aa-8812-323496c658ac",
    "csm-hit": "tb:F2R7RY9KHW9QD6FJKM1J+s-35RF3HYXQ35V642NEJMM|1753381826102&t:1753381826102&adb:adblk_no",
    "rxc": "AFwMp0lHQYisQR794Es"
}

# 🔧 Stato precedente
last_seen_items = set()

# 📩 Funzione Telegram
def send_telegram_message(msg: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Manca TOKEN o CHAT_ID")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}
        )
    except Exception as e:
        print("Errore Telegram:", e)

# 🔎 Monitoraggio
def monitor_page():
    global last_seen_items
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=headers, cookies=COOKIES)
        soup = BeautifulSoup(r.text, "html.parser")

        # 👇 Cambia selettore se serve
        current_items = set([el.text.strip() for el in soup.find_all("h2") if el.text.strip()])

        if not last_seen_items:
            last_seen_items.update(current_items)
            print("✅ Stato iniziale salvato.")
            return

        # Nuovi prodotti
        new_items = current_items - last_seen_items
        for item in new_items:
            send_telegram_message(f"🆕 Nuovo articolo Vine trovato: {item}")

        # Prodotti rimossi
        removed_items = last_seen_items - current_items
        for item in removed_items:
            send_telegram_message(f"❌ Prodotto rimosso: {item}")

        # Aggiorna stato
        last_seen_items.clear()
        last_seen_items.update(current_items)

        if not new_items and not removed_items:
            print("🔄 Nessuna modifica trovata.")

    except Exception as e:
        print("❌ Errore monitoraggio:", e)

# 🌐 Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MonitorVine attivo e funzionante!"

# 🚀 Thread monitor
def run_monitor():
    while True:
        monitor_page()
        time.sleep(600)  # ogni 10 minuti

threading.Thread(target=run_monitor, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

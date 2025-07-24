import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
import threading

# 🔑 Inseriamo direttamente qui i tuoi dati Telegram
TELEGRAM_TOKEN = "7531290365:AAGx-n2XkPOKwA_tBNvVEYTBxQJhnZ5l4sY"
TELEGRAM_CHAT_ID = "495561018"

# 🌍 URL da monitorare
URL = "https://www.amazon.it/vine/vine-items?queue=potluck"

last_seen_items = set()

# 🔧 Funzione per inviare messaggi su Telegram
def send_telegram_message(message: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        resp = requests.post(url, data=data)
        print("Telegram response:", resp.text)
    except Exception as e:
        print("Errore nell'invio del messaggio Telegram:", e)

# 🔎 Funzione di monitoraggio
def monitor_page():
    global last_seen_items
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # 👇 ATTENZIONE: selettore degli articoli, puoi adattarlo se serve
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

# 🖥️ Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MonitorVine attivo!"

# 🚀 Avvio monitoraggio in background
def run_monitor():
    while True:
        monitor_page()
        time.sleep(600)  # ogni 10 minuti

threading.Thread(target=run_monitor, daemon=True).start()

if __name__ == '__main__':
    port = 5000
    app.run(host="0.0.0.0", port=port)

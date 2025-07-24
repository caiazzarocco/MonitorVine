import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
import threading

# 🔑 Variabili Telegram prese dalle Environment Variables su Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 🌍 URL di test pubblico
URL = "https://time.is/"

# Stato precedente degli elementi
last_seen_items = set()

# 🔧 Funzione per inviare messaggi su Telegram
def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ TOKEN o CHAT_ID mancanti.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print(f"📩 Inviato su Telegram: {message}")
    except Exception as e:
        print("❌ Errore invio Telegram:", e)

# 🔎 Funzione per monitorare la pagina
def monitor_page():
    global last_seen_items
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # 🔥 Selettore generico, prende tutto il testo nei div
        items = set([el.text.strip() for el in soup.find_all("div")])

        if not last_seen_items:
            last_seen_items = items
            print("✅ Stato iniziale salvato.")
            return

        new_items = items - last_seen_items
        if new_items:
            for item in new_items:
                send_telegram_message(f"🆕 Nuovo elemento trovato: {item}")
            last_seen_items = items
        else:
            print("🔄 Nessun nuovo elemento trovato.")
    except Exception as e:
        print("❌ Errore monitoraggio:", e)

# 🖥️ Flask per mantenere attivo il servizio
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MonitorVine TEST (1 minuto) attivo!"

# 🚀 Avvio monitoraggio in background
def run_monitor():
    while True:
        monitor_page()
        time.sleep(60)  # intervallo di 1 minuto

threading.Thread(target=run_monitor, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

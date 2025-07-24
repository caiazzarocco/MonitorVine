import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask

# 🔑 Variabili ambiente da inserire su Render nelle Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 🌍 URL da monitorare
URL = "https://www.amazon.it/vine/vine-items?queue=potluck"

# Salva l'ultimo stato per confrontare i cambiamenti
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

        # 👇 Qui dovresti mettere un selettore specifico per i prodotti
        items = set([el.text.strip() for el in soup.find_all("h2")])  # esempio generico

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

# 🖥️ Flask app per mantenere il servizio attivo su Render
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ MonitorVine attivo!"

# 🚀 Avvio monitoraggio in background
import threading

def run_monitor():
    while True:
        monitor_page()
        time.sleep(600)  # 600 secondi = 10 minuti

threading.Thread(target=run_monitor, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

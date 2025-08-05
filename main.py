import os
import requests

# 🔐 Legge le variabili ambiente da Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 📤 Funzione per inviare messaggi su Telegram
def send_telegram_message(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Manca TELEGRAM_TOKEN o TELEGRAM_CHAT_ID.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Messaggio inviato con successo.")
        else:
            print(f"⚠️ Errore nell'invio. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore Telegram: {e}")

# ▶️ Avvio del test
if __name__ == "__main__":
    send_telegram_message("✅ Test riuscito! Il tuo bot Telegram è attivo.")

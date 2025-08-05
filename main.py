import os
import requests

chat_id = os.environ.get("TELEGRAM_CHAT_ID")
token = os.environ.get("TELEGRAM_TOKEN")

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg
    }
    response = requests.post(url, data=payload)
    print("Telegram response:", response.text)

send_telegram_message("✅ Test messaggio da Render. Funziona tutto!")

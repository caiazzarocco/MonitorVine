import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_test_message():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Manca TELEGRAM_TOKEN o TELEGRAM_CHAT_ID")
        return
    message = "✅ Test messaggio da Render riuscito!"
    url = f"https://api.telegram.org/{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    print(f"Telegram response: {response.status_code} - {response.text}")

@app.route('/')
def home():
    send_test_message()
    return "✅ Test Telegram Inviato!"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

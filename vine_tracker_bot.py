import requests
import time
import os
from bs4 import BeautifulSoup
from telegram import Bot

# CONFIGURAZIONE
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = "https://www.amazon.it/vine/vine-items?queue=potluck"
CHECK_INTERVAL = 300  # ogni 5 minuti

# STATO
previous_products = set()

# FUNZIONE PER ESTRARRE PRODOTTI
def fetch_current_products():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('div.a-section.a-spacing-base.potluck-item')
    product_names = set()
    for item in items:
        title_el = item.select_one('span.a-text-normal')
        if title_el:
            product_names.add(title_el.text.strip())
    return product_names

# AVVIO BOT
bot = Bot(token=TELEGRAM_TOKEN)
print("✅ Monitoraggio attivo...")

while True:
    try:
        current_products = fetch_current_products()
        new_products = current_products - previous_products
        removed_products = previous_products - current_products

        for product in new_products:
            bot.send_message(chat_id=CHAT_ID, text=f"🟢 Nuovo prodotto Vine:
{product}")
        for product in removed_products:
            bot.send_message(chat_id=CHAT_ID, text=f"🔴 Prodotto rimosso da Vine:
{product}")

        previous_products = current_products
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"❌ Errore nel monitoraggio: {str(e)}")
        print("Errore:", e)

    time.sleep(CHECK_INTERVAL)

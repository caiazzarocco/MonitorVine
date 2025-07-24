import requests, time, hashlib

# 🔧 CONFIGURAZIONE GENERALE
URL = "https://www.amazon.it/vine/vine-items?queue=potluck"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    # 👇 Cookie Amazon estratti con EditThisCookie (tutti su una riga)
    "Cookie": "at-acbit=Atza|IwEBIE9j4r49by1fmMZeYK4eybZUwaWL5lvVkOWzeWo1XKhWddPd7ebE3nUGN0sA0j6lY2xiDuPcKebu-laSa2c1zVmDpGqbqsrEHcLVqTzicv2Rkxh-ZcdRonEKOIj1gIjGcyK-cHDbQajMeN0SLJFPSlh9xL-EjaUi8gEbmvIK8vTtr3lJuN3OnUduQBKyEcsGxjtsqCLdJHkD4erAN9zcxn650IyEK75OQ_GpTdNf2XBnnw; i18n-prefs=EUR; lc-acbit=it_IT; sess-at-acbit=Wt327DM8nl65mQ1I4WC9Gn8iHCV/S196CA/RPr0JaXc=; session-id=260-8513997-2586068; session-id-time=2082787201l; session-token=oyq2Iv+K+Rqi9rnw7IfhRx7eerisZCIMp1mNlPBCL9eJvfftjTHLWC2CFgnf+9bY9Z8Ble2iUCIN91ZET4ZK3WGAae7NXYyGDZ//opqfKQxZFO2Dg7Q+FnIaTVzswTghc2oVEx/SQPIvSOKhXqQdgupWvPn4yf1R+88E2yrm5M35z4RTWtv1sbNnMc0LNaHxfwtL7sAxKcxv2AV6P/vnrByAWlx0kX2qYF6gi0XNfX3SUghGZwL77gYSO9kKa7DvJDqyMeoLI7zxkMzOmz+YsBiinrt6e0XcmurXf5RS/fpsMdK2QlIw6mVJWMQD3Uip9KrrqLdfWoRS4/OmZF/+ILMC9ADLKzJEWQ0m4V+7jvh0+0D8S8BT49nVdezm7kO+; sst-acbit=Sst1|PQHurXazfrEOvAQvCT6rQz6xDFHGanFRIra0Opozqum_fV3vAiQRmDd_MUdFel8Nc8iCe2uWUbyAarQQ-VO1Kz29xUt_59__fd3uI11hDuKeZSvrXwhBVB3QpaAl3Fav-AK3nmAJBSoo9jOK-JJx15KI2KkVS5JzPCELlZnOp1DnACjGgfSfxH5v_g8lfhWV7CbeVKXIGaCqvf-WuRzCWwQSlr26moPU8W4SO3XjPN9twNldzA8_HTuSO9rxFm11FqX3p6wk_Swisc5FrYxPnobKeU2aJvH1niD7CyR6IAY3iK7Hdt6Bg4yTiytVJtURQQzTAhwEXOx-d3phE750OsbGmlsGGUEMSsnCYZRzRP8hvFo; ubid-acbit=261-9368406-4193301; x-acbit=\"AYk1pUfYdflO5KCkdW0L3Bj9hDb9fpUhnTj8rq96JrJqI@mflnN4xl6KQoJjgsgy\"; cwr_u=080ec2f6-5f68-47aa-8812-323496c658ac; csm-hit=tb:2D2PAJCJ5CNS7RTZSCZA+s-JRQDKQCD8QGRREPFDZCR|1753294325896&t:1753294325896&adb:adblk_no; rxc=AFwMp0l8H4usQR79t0s"
}

# 🔑 Token e Chat ID del tuo bot Telegram
TOKEN = "7531290365:AAGx-n2XkPOKwA_tBNvVEYTBxQJhnZ5l4sY"
CHAT_ID = "495561018"

# ⏳ Intervallo di aggiornamento in secondi (600 = 10 minuti)
INTERVALLO = 600

def invia_notifica(messaggio):
    """Invia una notifica su Telegram."""
    url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url_telegram, data={"chat_id": CHAT_ID, "text": messaggio})
        print("✅ Notifica inviata:", r.text)
    except Exception as err:
        print("❌ Errore nell'invio della notifica:", err)

def leggi_pagina():
    """Scarica il contenuto della pagina Vine."""
    r = requests.get(URL, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text

print("👀 Avvio monitoraggio della pagina Vine...")

hash_prec = ""

while True:
    try:
        contenuto = leggi_pagina()
        nuovo_hash = hashlib.md5(contenuto.encode("utf-8")).hexdigest()

        if hash_prec and nuovo_hash != hash_prec:
            invia_notifica("✅ La pagina Vine si è aggiornata! Controlla subito:\n" + URL)

        hash_prec = nuovo_hash
    except Exception as e:
        invia_notifica(f"⚠️ Errore durante il controllo: {e}")

    time.sleep(INTERVALLO)

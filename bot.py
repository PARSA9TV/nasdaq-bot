import requests
import time

TELEGRAM_BOT_TOKEN = "8460415001:AAEb6f2QZqW33x6f7cDcfTvRL-qRqNpJrdo"
CHAT_ID = "1667933952"

API = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL,TSLA,MSFT,NVDA"

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

old_prices = {}

while True:
    try:
        data = requests.get(API).json()
        quotes = data["quoteResponse"]["result"]

        for q in quotes:
            symbol = q["symbol"]
            price = q.get("regularMarketPrice", 0)

            if symbol not in old_prices:
                old_prices[symbol] = price

            change = price - old_prices[symbol]

            # Fiyat artışı uyarısı
            if change > 0.5:
                send(f"🚀 {symbol} yükseliyor! +{change:.2f} USD")

            old_prices[symbol] = price

        time.sleep(10)

    except Exception as e:
        send(f"Hata: {e}")
        time.sleep(10)

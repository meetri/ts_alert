import requests
from os import environ
import json
from flask import Flask, request
from telegram.ext import Updater

app = Flask(__name__)

SECURE_KEY = environ.get("secure_key", "abc123")
bot_token = environ.get("bot_token")
bot_chatID = environ.get("chat_id")


def notify_channel(alertname, symbol, payload):
    print(alertname)
    print(symbol)
    print(payload)

    bot_message = f"*Trendspider Alert*: `{symbol}` {alertname} - {payload}"
    telegram_url = f"https://api.telegram.org/bot{bot_token}/"
    message = f'sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'

    response = requests.get(f"{telegram_url}{message}")
    r = response.json()
    print(r)


@app.route('/robot/ts/trigger', methods=['POST'])  # Create main page of web-application
def ts_trigger():

    securekey = request.args.get('secure', SECURE_KEY)
    alertname = request.args.get('name')
    symbol = request.args.get('symbol')
    note = request.args.get('note')

    if request.is_json:
        payload = request.get_json()
    else:
        payload = request.get_data(as_text=True)

    if securekey == SECURE_KEY:
        notify_channel(alertname, symbol, payload)
        print(f"name={alertname}, symbol={symbol}, note={note}, payload={payload}")

    return f"Welcome to my API! - {payload}/{symbol}"


if __name__ == '__main__':
    notify_channel("", "success", "Trendspider chart notifier installed")
    app.run()

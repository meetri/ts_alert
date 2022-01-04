import requests
from os import environ
import json
from flask import Flask, request

app = Flask(__name__)

SECURE_KEY = environ.get("secure_key")
bot_token = environ.get("bot_token")
bot_chatID = environ.get("chat_id")
PORT = int(environ.get("PORT", "5000"))

def notify_integromat_direct(symbol, alertname, alertnote):
    url = "https://hook.integromat.com/eto368pdouscc7hvxfyoy38fj1yvcsrq"
    r = requests.post(f"{url}?symbol={symbol}", data={
        "symbol": symbol,
        "alertname": alertname,
        "alertnote": alertnote
    })
    print(r.text)

def notify_integromat(symbol, alertname, alertnote):
    url = "https://hook.integromat.com/eto368pdouscc7hvxfyoy38fj1yvcsrq"
    r = requests.post(
            f"{url}?symbol={symbol}&name={alertname}&note={alertnote}",
            data=alertnote)
    print(r.text)

def notify_channel(alertname, symbol, payload):
    bot_message = f"*Trendspider Alert*: `{symbol}` {alertname} - {payload}"
    print(bot_message)
    telegram_url = f"https://api.telegram.org/bot{bot_token}/"
    message = f'sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'

    response = requests.get(f"{telegram_url}{message}")
    r = response.json()
    print(r)

    return r


@app.route('/landbot/parse_incoming', methods=['POST'])
def parse_landbot():
    payload = request.get_json()

    max_columns = 2
    for message in payload.get("messages", []):
        buttons = message.get("buttons", [])
        callbacks = message.get("payloads", [])
        keyboards = []
        krow = []
        for idx, _ in enumerate(buttons):
            krow.append(
                {"text": buttons[idx], "callback_data": callbacks[idx]}
             )
            if len(krow) == max_columns:
                keyboards.append(krow.copy())
                krow.clear()

        if len(krow):
            keyboards.append(krow)

        if len(keyboards):
            message["inline_keyboard"] = json.dumps({
                "inline_keyboard": keyboards
            })

    return payload


@app.route('/', methods=['GET'])  # Create main page of web-application
def greeting():
    return "Hello"


@app.route('/robot/ts/trigger', methods=['POST'])
def ts_trigger():
    securekey = request.args.get('secure_key')
    alertname = request.args.get('name')
    symbol = request.args.get('symbol')
    note = request.args.get('note')

    if request.is_json:
        payload = request.get_json()
    else:
        payload = request.get_data(as_text=True)

    if securekey == SECURE_KEY:
        notify_integromat(symbol, alertname, payload)
        # notify_channel(alertname, symbol, payload)
        print(f"name={alertname}, symbol={symbol}, note={note}, payload={payload}")

    return f"Welcome to my API! - {payload}/{symbol}"


print(f"starting app: [{__name__}]:{PORT}")
if __name__ == '__main__':
    # notify_channel("", "success", "Trendspider chart notifier installed")
    notify_integromat("success", "myalert", "Trendspider notifier installed")
    app.run(host="0.0.0.0", port=PORT)
    print("why did it exit?")

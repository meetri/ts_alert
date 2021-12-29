import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')  # Create main page of web-application
def index():
    payload = request.get_json()
    args = request.args
    print(f"payload={payload}, args={args}")
    return f"Welcome to my API! - {payload}/{args}"


if __name__ == '__main__':
    app.run()

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')  # Create main page of web-application
def index():
    data = request.get_data()
    print(data)
    return f"Welcome to my API! - {data}"


if __name__ == '__main__':
    app.run()

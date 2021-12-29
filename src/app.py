import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/') # Create main page of web-application
def index():
    return "Welcome to my API!" # Display text on main page


if __name__ == '__main__':
    app.run() # Run the application

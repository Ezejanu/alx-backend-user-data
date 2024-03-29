#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """
    Route handler for the root endpoint.

    Returns:
        dict: A JSON payload with a welcome message.
    """

    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    """
    This block of code runs the Flask app when the script is executed directly.
    """
    app.run(host="0.0.0.0", port="5000")

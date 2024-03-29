#!/usr/bin/env python3

from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


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


@app.route("/users", methods=["POST"])
def register_user():
    """
    Route handler for registering a new user.

    Expects two form data fields: "email" and "password".
    If the user does not exist, register it and respond with a success message.
    If the user is already registered, return an error message.

    Returns:
        dict: JSON response containing the result of user registration.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    """
    This block of code runs the Flask app when the script is executed directly.
    """
    app.run(host="0.0.0.0", port="5000")

"""
Controller for handling user login functionality.
"""

from flask import request, jsonify, Blueprint
from auth.services.login_service import LoginService

login_controller = Blueprint("login_controller", __name__)
login_service = LoginService()

@login_controller.route("/login", methods=["POST"])
def login_user():
    """
    Endpoint for user login.
    Validates login credentials and generates a session token.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    session_token = login_service.authenticate_user(email, password)
    if session_token:
        return jsonify({"message": "Login successful", "token": session_token}), 200

    return jsonify({"error": "Invalid email or password"}), 401
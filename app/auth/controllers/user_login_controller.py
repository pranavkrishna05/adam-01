"""
Controller for handling user login functionality.
"""

from flask import request, jsonify, Blueprint
from auth.services.user_login_service import UserLoginService

user_login_controller = Blueprint("user_login_controller", __name__)
user_login_service = UserLoginService()

@user_login_controller.route("/login", methods=["POST"])
def login_user():
    """
    Endpoint to log in a user and start a session.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    login_response = user_login_service.authenticate_user(email, password)
    if login_response:
        return jsonify({"message": "Login successful", "session_token": login_response}), 200

    return jsonify({"error": "Invalid email or password"}), 401
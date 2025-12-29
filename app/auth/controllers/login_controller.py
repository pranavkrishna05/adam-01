"""
Controller for handling user login and session management.
"""

from flask import request, jsonify, Blueprint, session
from auth.services.login_service import LoginService
from datetime import timedelta

login_controller = Blueprint("login_controller", __name__)
login_service = LoginService()

SESSION_TIMEOUT_MINUTES = 30

@login_controller.route("/auth/login", methods=["POST"])
def login_user():
    """
    Endpoint for authenticating user credentials and starting a session.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = login_service.authenticate_user(email=email, password=password)
        session["user_id"] = user.id
        session.permanent = True
        login_controller.permanent_session_lifetime = timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500


@login_controller.route("/auth/logout", methods=["POST"])
def logout_user():
    """
    Endpoint for user logout and session termination.
    """
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully"}), 200
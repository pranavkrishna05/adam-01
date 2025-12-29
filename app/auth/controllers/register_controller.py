"""
Controller for handling user registration and account creation with enhanced security.
"""

from flask import request, jsonify, Blueprint
from auth.services.register_service import RegisterService
from captcha import verify_captcha

register_controller = Blueprint("register_controller", __name__)
register_service = RegisterService()

@register_controller.route("/auth/register", methods=["POST"])
def register_user():
    """
    Endpoint for user registration.
    Validates input, ensures email uniqueness and password security, and validates captcha response.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    captcha_response = data.get("captcha_response")

    if not (email and password and captcha_response):
        return jsonify({"error": "Email, password, and captcha response are required"}), 400

    if not verify_captcha(captcha_response):
        return jsonify({"error": "Invalid captcha response"}), 400

    try:
        user = register_service.register_user(email=email, password=password)
        return jsonify({"message": "User registered successfully", "user_id": user.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Registration failed"}), 500
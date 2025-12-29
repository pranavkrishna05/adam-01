"""
Controller for handling user registration and account creation.
"""

from flask import request, jsonify, Blueprint
from auth.services.register_service import RegisterService

register_controller = Blueprint("register_controller", __name__)
register_service = RegisterService()

@register_controller.route("/auth/register", methods=["POST"])
def register_user():
    """
    Endpoint for user registration.
    Validates input, ensures email uniqueness and password security.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = register_service.register_user(email=email, password=password)
        return jsonify({"message": "User registered successfully", "user_id": user.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Registration failed"}), 500
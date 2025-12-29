"""
Controller for handling user registration.
"""

from flask import request, jsonify, Blueprint
from auth.services.registration_service import RegistrationService

registration_controller = Blueprint("registration_controller", __name__)
registration_service = RegistrationService()

@registration_controller.route("/register", methods=["POST"])
def register_user():
    """
    Endpoint for user registration.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not registration_service.is_password_secure(password):
        return jsonify({"error": "Password does not meet security criteria"}), 400

    user = registration_service.create_user(email, password)
    if user:
        return jsonify({"message": "User registered successfully", "user": user.dict()}), 201

    return jsonify({"error": "Email already exists"}), 400
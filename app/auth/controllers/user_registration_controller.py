"""
Controller for handling user registration.
"""

from flask import request, jsonify, Blueprint
from auth.services.user_registration_service import UserRegistrationService

user_registration_controller = Blueprint("user_registration_controller", __name__)
user_registration_service = UserRegistrationService()

@user_registration_controller.route("/register", methods=["POST"])
def register_user():
    """
    Endpoint to register a new user with email and password.
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not user_registration_service.is_password_secure(password):
        return jsonify({"error": "Password does not meet security criteria"}), 400

    if user_registration_service.is_email_taken(email):
        return jsonify({"error": "Email is already in use"}), 400

    user = user_registration_service.create_user(email, password)
    return jsonify(user.dict()), 201
"""
Controller for handling password reset functionality.
"""

from flask import request, jsonify, Blueprint
from auth.services.password_reset_service import PasswordResetService

password_reset_controller = Blueprint("password_reset_controller", __name__)
password_reset_service = PasswordResetService()

@password_reset_controller.route("/password-reset/request", methods=["POST"])
def request_password_reset():
    """
    Endpoint to request a password reset link.
    """
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    reset_success = password_reset_service.send_reset_email(email)
    if reset_success:
        return jsonify({"message": "Password reset email sent"}), 200

    return jsonify({"error": "Email not found"}), 404

@password_reset_controller.route("/password-reset", methods=["POST"])
def reset_password():
    """
    Endpoint to reset the user's password using the reset token.
    """
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    if not password_reset_service.is_password_secure(new_password):
        return jsonify({"error": "Password does not meet security criteria"}), 400

    reset_success = password_reset_service.reset_password(token, new_password)
    if reset_success:
        return jsonify({"message": "Password reset successfully"}), 200

    return jsonify({"error": "Invalid or expired token"}), 400
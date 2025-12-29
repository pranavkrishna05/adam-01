"""
Controller for managing password reset functionality.
"""

from flask import request, jsonify, Blueprint
from auth.services.password_reset_service import PasswordResetService

password_reset_controller = Blueprint("password_reset_controller", __name__)
password_reset_service = PasswordResetService()

@password_reset_controller.route("/password-reset", methods=["POST"])
def request_password_reset():
    """
    Endpoint to request a password reset link.
    Sends an email with a password reset link to the user.
    """
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    link_sent = password_reset_service.send_reset_link(email)
    if link_sent:
        return jsonify({"message": "Password reset link has been sent to your email"}), 200
    return jsonify({"error": "Failed to send reset link. Make sure the email is registered."}), 404

@password_reset_controller.route("/password-reset/<token>", methods=["POST"])
def reset_password(token):
    """
    Endpoint to reset the password using a token.
    The token expires after 24 hours.
    """
    data = request.json
    new_password = data.get("password")

    if not new_password:
        return jsonify({"error": "New password is required"}), 400

    if not password_reset_service.is_password_secure(new_password):
        return jsonify({"error": "Password does not meet security criteria"}), 400

    reset_successful = password_reset_service.reset_password(token, new_password)
    if reset_successful:
        return jsonify({"message": "Password has been successfully updated"}), 200
    return jsonify({"error": "Invalid or expired token"}), 400
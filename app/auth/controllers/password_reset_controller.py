"""
Controller for handling password reset requests and token validation.
"""

from flask import request, jsonify, Blueprint
from auth.services.password_reset_service import PasswordResetService

password_reset_controller = Blueprint("password_reset_controller", __name__)
password_reset_service = PasswordResetService()

@password_reset_controller.route("/auth/request-password-reset", methods=["POST"])
def request_password_reset():
    """
    Endpoint to request a password reset link.
    Verifies user email and sends a secure token-based reset link.
    """
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        password_reset_service.initiate_reset(email)
        return jsonify({"message": "Password reset link sent to your email"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to send password reset link"}), 500


@password_reset_controller.route("/auth/reset-password", methods=["POST"])
def reset_password():
    """
    Endpoint to reset the password using a valid token.
    """
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    try:
        password_reset_service.reset_password(token, new_password)
        return jsonify({"message": "Password reset successful"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Password reset failed"}), 500
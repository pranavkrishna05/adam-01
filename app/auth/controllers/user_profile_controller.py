"""
Controller for handling user profile management.
"""

from flask import request, jsonify, Blueprint
from auth.services.user_profile_service import UserProfileService

user_profile_controller = Blueprint("user_profile_controller", __name__)
user_profile_service = UserProfileService()

@user_profile_controller.route("/profile", methods=["GET"])
def get_profile():
    """
    Endpoint to retrieve the user's profile information.
    """
    user_email = request.headers.get("User-Email")

    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    profile = user_profile_service.get_user_profile(user_email)
    if profile:
        return jsonify(profile.dict()), 200
    return jsonify({"error": "Profile not found"}), 404

@user_profile_controller.route("/profile", methods=["PUT"])
def update_profile():
    """
    Endpoint to update the user's profile information.
    """
    user_email = request.headers.get("User-Email")
    if not user_email:
        return jsonify({"error": "User email is required"}), 400

    data = request.json
    updated_profile = user_profile_service.update_user_profile(user_email, data)
    if updated_profile:
        return jsonify(updated_profile.dict()), 200
    return jsonify({"error": "Unable to update profile"}), 400
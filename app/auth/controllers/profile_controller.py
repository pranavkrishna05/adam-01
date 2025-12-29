"""
Controller for managing user profile updates.
"""

from flask import request, jsonify, Blueprint
from auth.services.profile_service import ProfileService
from auth.models.user_model import User

profile_controller = Blueprint("profile_controller", __name__)
profile_service = ProfileService()

@profile_controller.route("/profile", methods=["GET"])
def get_profile():
    """
    Endpoint to retrieve user profile information.
    """
    user_id = request.headers.get("User-ID")  # Assume user authentication provides a valid user ID.
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    profile = profile_service.get_user_profile(int(user_id))
    if profile:
        return jsonify(profile.dict()), 200

    return jsonify({"error": "User not found"}), 404

@profile_controller.route("/profile", methods=["PUT"])
def update_profile():
    """
    Endpoint to update user profile information.
    """
    user_id = request.headers.get("User-ID")  # Assume user authentication provides a valid user ID.
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    data = request.json
    name = data.get("name")
    preferences = data.get("preferences")

    if not name and not preferences:
        return jsonify({"error": "At least one field (name or preferences) must be provided"}), 400

    updated_profile = profile_service.update_user_profile(int(user_id), name, preferences)
    if updated_profile:
        return jsonify(updated_profile.dict()), 200

    return jsonify({"error": "Failed to update profile"}), 404
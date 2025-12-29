"""
Controller for managing user profile updates and retrieval.
"""

from flask import request, jsonify, Blueprint
from auth.services.profile_service import ProfileService

profile_controller = Blueprint("profile_controller", __name__)
profile_service = ProfileService()


@profile_controller.route("/auth/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    """
    Endpoint to retrieve user profile details.
    """
    try:
        profile = profile_service.get_profile(user_id)
        return jsonify(profile.dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Failed to retrieve profile"}), 500


@profile_controller.route("/auth/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    """
    Endpoint to update user profile information.
    Returns updated profile upon success.
    """
    data = request.json
    try:
        updated_profile = profile_service.update_profile(user_id, data)
        return jsonify(updated_profile.dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to update profile"}), 500
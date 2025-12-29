"""
Controller for saving and retrieving a user's shopping cart state.
"""

from flask import Blueprint, request, jsonify
from cart.services.cart_persistence_service import CartPersistenceService

cart_persistence_controller = Blueprint("cart_persistence_controller", __name__)
cart_persistence_service = CartPersistenceService()


@cart_persistence_controller.route("/cart/save", methods=["POST"])
def save_cart_state():
    """
    Saves the current user's cart state to their profile.
    Requires authentication (user_id header required).
    """
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    try:
        cart_state = cart_persistence_service.save_cart_state(user_id)
        return jsonify({
            "message": "Cart state saved successfully",
            "cart": cart_state
        }), 200
    except Exception:
        return jsonify({"error": "Failed to save cart state"}), 500


@cart_persistence_controller.route("/cart/load", methods=["GET"])
def load_cart_state():
    """
    Loads the saved cart state from the user's profile.
    Allows the user to restore their cart across sessions.
    """
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    try:
        cart = cart_persistence_service.load_cart_state(user_id)
        if cart is None:
            return jsonify({"message": "No saved cart found"}), 404
        return jsonify({"message": "Cart loaded successfully", "cart": cart}), 200
    except Exception:
        return jsonify({"error": "Failed to load cart"}), 500
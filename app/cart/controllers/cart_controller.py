"""
Controller for managing shopping cart operations.
"""

from flask import Blueprint, request, jsonify
from cart.services.cart_service import CartService

cart_controller = Blueprint("cart_controller", __name__)
cart_service = CartService()


@cart_controller.route("/cart", methods=["GET"])
def view_cart():
    """
    View current user's cart contents.
    For logged-in users, retrieves persistent cart.
    For guests, retrieves session cart.
    """
    user_id = request.headers.get("X-User-Id")
    session_id = request.cookies.get("session_id")

    try:
        cart = cart_service.get_cart(user_id=user_id, session_id=session_id)
        return jsonify(cart), 200
    except Exception:
        return jsonify({"error": "Failed to retrieve cart"}), 500


@cart_controller.route("/cart/add", methods=["POST"])
def add_to_cart():
    """
    Add a product to the user's cart.
    If the user is logged in, it persists across sessions.
    For guest users, it is bound to their current session.
    """
    data = request.json
    if not data or "product_id" not in data or "quantity" not in data:
        return jsonify({"error": "product_id and quantity are required"}), 400

    user_id = request.headers.get("X-User-Id")
    session_id = request.cookies.get("session_id")
    try:
        updated_cart = cart_service.add_to_cart(
            product_id=data["product_id"],
            quantity=data["quantity"],
            user_id=user_id,
            session_id=session_id
        )
        return jsonify({"message": "Product added to cart", "cart": updated_cart}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to add item to cart"}), 500


@cart_controller.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    """
    Remove a product from the user's cart.
    """
    data = request.json
    if not data or "product_id" not in data:
        return jsonify({"error": "product_id is required"}), 400

    user_id = request.headers.get("X-User-Id")
    session_id = request.cookies.get("session_id")
    try:
        updated_cart = cart_service.remove_from_cart(
            product_id=data["product_id"],
            user_id=user_id,
            session_id=session_id
        )
        return jsonify({"message": "Product removed from cart", "cart": updated_cart}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to remove item from cart"}), 500
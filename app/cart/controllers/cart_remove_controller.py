"""
Controller for removing products from the shopping cart.
"""

from flask import Blueprint, request, jsonify
from cart.services.cart_remove_service import CartRemoveService

cart_remove_controller = Blueprint("cart_remove_controller", __name__)
cart_remove_service = CartRemoveService()


@cart_remove_controller.route("/cart/remove", methods=["POST"])
def remove_cart_item():
    """
    Endpoint to remove a product from the shopping cart.
    Requires a confirmation flag to ensure intentional removal.
    Automatically recalculates total cart price.
    """
    data = request.json
    user_id = request.headers.get("X-User-Id")
    session_id = request.cookies.get("session_id")

    if not data or "product_id" not in data:
        return jsonify({"error": "product_id is required"}), 400

    if data.get("confirm") != True:
        return jsonify({"error": "Removal not confirmed. Confirm=true required."}), 400

    try:
        updated_cart = cart_remove_service.remove_item(
            product_id=data["product_id"],
            user_id=user_id,
            session_id=session_id
        )
        return jsonify({
            "message": "Item removed successfully",
            "cart": updated_cart
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to remove item from cart"}), 500
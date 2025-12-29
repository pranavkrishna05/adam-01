"""
Controller for updating quantities of products in the shopping cart.
"""

from flask import Blueprint, request, jsonify
from cart.services.cart_update_service import CartUpdateService

cart_update_controller = Blueprint("cart_update_controller", __name__)
cart_update_service = CartUpdateService()


@cart_update_controller.route("/cart/update", methods=["POST"])
def update_cart_item_quantity():
    """
    Updates the quantity of a product in the shopping cart.
    Quantity must be a positive integer.
    Automatically recalculates the total cart price.
    """
    data = request.json
    user_id = request.headers.get("X-User-Id")
    session_id = request.cookies.get("session_id")

    if not data or "product_id" not in data or "quantity" not in data:
        return jsonify({"error": "product_id and quantity are required"}), 400

    quantity = data["quantity"]
    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    try:
        updated_cart = cart_update_service.update_quantity(
            product_id=data["product_id"],
            quantity=quantity,
            user_id=user_id,
            session_id=session_id,
        )
        return jsonify({
            "message": "Quantity updated successfully",
            "cart": updated_cart
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to update product quantity"}), 500
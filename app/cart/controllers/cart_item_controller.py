"""
Controller to handle removing items from the shopping cart.
"""

from flask import request, jsonify, Blueprint
from cart.services.cart_item_service import CartItemService

cart_item_controller = Blueprint("cart_item_controller", __name__)
cart_item_service = CartItemService()

@cart_item_controller.route("/cart/<int:product_id>", methods=["DELETE"])
def remove_item(product_id):
    """
    Endpoint to remove a product from the user's shopping cart.
    Requires confirmation from the user.
    """
    user_id = request.headers.get("User-ID")
    confirmation = request.args.get("confirmation")

    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    if confirmation != "CONFIRM":
        return jsonify({"error": "Confirmation is required to delete the item"}), 400

    success = cart_item_service.remove_item(user_id, product_id)
    if success:
        return jsonify({"message": "Product removed from the cart successfully"}), 200

    return jsonify({"error": "Failed to remove the product or product not found in the cart"}), 404
"""
Controller for managing product quantity modifications in the shopping cart.
"""

from flask import request, jsonify, Blueprint
from cart.services.cart_quantity_service import CartQuantityService

cart_quantity_controller = Blueprint("cart_quantity_controller", __name__)
cart_quantity_service = CartQuantityService()

@cart_quantity_controller.route("/cart/<int:product_id>", methods=["PUT"])
def update_quantity(product_id):
    """
    Endpoint to modify the quantity of a product in the shopping cart.
    """
    user_id = request.headers.get("User-ID")
    data = request.json
    quantity = data.get("quantity")

    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    if quantity is None or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    success = cart_quantity_service.update_quantity(user_id, product_id, quantity)
    if success:
        return jsonify({"message": "Product quantity updated successfully"}), 200

    return jsonify({"error": "Product not found in the cart or update failed"}), 404
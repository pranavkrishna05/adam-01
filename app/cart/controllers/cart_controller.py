"""
Controller for managing shopping cart functionality.
"""

from flask import request, jsonify, Blueprint
from cart.services.cart_service import CartService

cart_controller = Blueprint("cart_controller", __name__)
cart_service = CartService()

@cart_controller.route("/cart", methods=["GET"])
def get_cart():
    """
    Endpoint to retrieve the current shopping cart for the user.
    """
    user_id = request.headers.get("User-ID")
    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    cart = cart_service.get_cart(user_id)
    return jsonify(cart), 200


@cart_controller.route("/cart", methods=["POST"])
def add_to_cart():
    """
    Endpoint to add a product to the shopping cart.
    """
    data = request.json
    user_id = request.headers.get("User-ID")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    success = cart_service.add_to_cart(user_id, product_id, quantity)
    if success:
        return jsonify({"message": "Product added to cart successfully"}), 200

    return jsonify({"error": "Failed to add product to cart"}), 500


@cart_controller.route("/cart/<int:product_id>", methods=["DELETE"])
def remove_from_cart(product_id):
    """
    Endpoint to remove a product from the shopping cart.
    """
    user_id = request.headers.get("User-ID")
    if not user_id:
        return jsonify({"error": "User-ID header is required"}), 400

    success = cart_service.remove_from_cart(user_id, product_id)
    if success:
        return jsonify({"message": "Product removed from cart successfully"}), 200

    return jsonify({"error": "Failed to remove product from cart"}), 500
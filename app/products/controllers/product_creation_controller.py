"""
Controller for managing product creation.
"""

from flask import request, jsonify, Blueprint
from products.services.product_creation_service import ProductCreationService

product_creation_controller = Blueprint("product_creation_controller", __name__)
product_creation_service = ProductCreationService()

@product_creation_controller.route("/products", methods=["POST"])
def create_product():
    """
    Endpoint for adding a new product to the inventory.
    Only accessible to admin users.
    """
    data = request.json
    admin_token = request.headers.get("Admin-Token")

    if not product_creation_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    name = data.get("name")
    price = data.get("price")
    description = data.get("description")
    category_id = data.get("category_id")

    if not name or not description:
        return jsonify({"error": "Name and description are required"}), 400

    if product_creation_service.is_product_name_exists(name):
        return jsonify({"error": "Product name must be unique"}), 400

    if price is None or not product_creation_service.is_valid_price(price):
        return jsonify({"error": "Product price must be a valid positive number"}), 400

    new_product = product_creation_service.create_product(name, price, description, category_id)
    if new_product:
        return jsonify(new_product.dict()), 201

    return jsonify({"error": "Failed to add product"}), 500
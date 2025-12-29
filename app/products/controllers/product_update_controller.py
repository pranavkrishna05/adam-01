"""
Controller for managing product updates.
"""

from flask import request, jsonify, Blueprint
from products.services.product_update_service import ProductUpdateService

product_update_controller = Blueprint("product_update_controller", __name__)
product_update_service = ProductUpdateService()

@product_update_controller.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Endpoint for updating an existing product.
    Only accessible to admin users.
    """
    data = request.json
    admin_token = request.headers.get("Admin-Token")

    if not product_update_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    if name and product_update_service.is_product_name_exists(product_id, name):
        return jsonify({"error": "Product name must be unique"}), 400

    if price is not None and not product_update_service.is_valid_price(price):
        return jsonify({"error": "Price must be a valid positive number"}), 400

    if description == "":
        return jsonify({"error": "Product description cannot be removed"}), 400

    updated_product = product_update_service.update_product(product_id, name, price, description)
    if updated_product:
        return jsonify(updated_product.dict()), 200

    return jsonify({"error": "Failed to update product or product not found"}), 404
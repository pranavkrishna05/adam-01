"""
Controller for handling product updates by admin.
"""

from flask import request, jsonify, Blueprint
from products.services.product_update_service import ProductUpdateService

product_update_controller = Blueprint("product_update_controller", __name__)
product_update_service = ProductUpdateService()

@product_update_controller.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Endpoint for an admin to update an existing product's details.
    """
    admin_token = request.headers.get("Admin-Token")
    
    if not product_update_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")
    category_id = data.get("category_id")

    if name and product_update_service.is_duplicate_name(product_id, name):
        return jsonify({"error": "Product name already exists"}), 400

    if price is not None and (not isinstance(price, (int, float)) or price <= 0):
        return jsonify({"error": "Product price must be a positive number"}), 400

    if description is not None and not description.strip():
        return jsonify({"error": "Product description cannot be empty"}), 400

    updated_product = product_update_service.update_product(product_id, name, price, description, category_id)
    if updated_product:
        return jsonify(updated_product.dict()), 200

    return jsonify({"error": "Failed to update product"}), 404
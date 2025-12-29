"""
Controller for managing product functionality.
"""

from flask import request, jsonify, Blueprint
from products.services.product_service import ProductService

product_controller = Blueprint("product_controller", __name__)
product_service = ProductService()

@product_controller.route("/products", methods=["POST"])
def add_product():
    """
    Endpoint for an admin to add a new product.
    """
    admin_token = request.headers.get("Admin-Token")
    
    if not product_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")
    category_id = data.get("category_id")

    if not name or not description:
        return jsonify({"error": "Product name and description are required"}), 400

    if not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "Product price must be a positive number"}), 400

    product = product_service.create_product(name, price, description, category_id)
    if product:
        return jsonify(product.dict()), 201

    return jsonify({"error": "Product with the same name already exists"}), 400

@product_controller.route("/products", methods=["GET"])
def list_products():
    """
    Endpoint to list all products in the inventory.
    """
    products = product_service.get_all_products()
    return jsonify([product.dict() for product in products]), 200
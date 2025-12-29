"""
Controller for handling product creation and management operations.
"""

from flask import request, jsonify, Blueprint
from products.services.product_service import ProductService

product_controller = Blueprint("product_controller", __name__)
product_service = ProductService()


@product_controller.route("/products", methods=["POST"])
def add_product():
    """
    Endpoint for adding a new product to the inventory.
    Validates name uniqueness, price, and description fields.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["name", "price", "description", "category"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        product = product_service.create_product(
            name=data["name"],
            price=data["price"],
            description=data["description"],
            category=data["category"],
        )
        return jsonify({"message": "Product created successfully", "product": product.dict()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to create product"}), 500
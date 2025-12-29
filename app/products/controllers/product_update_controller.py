"""
Controller for handling product update operations by admin.
"""

from flask import request, jsonify, Blueprint
from products.services.product_update_service import ProductUpdateService

product_update_controller = Blueprint("product_update_controller", __name__)
product_update_service = ProductUpdateService()


@product_update_controller.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id: int):
    """
    Endpoint for updating existing product details.
    Only accessible by admin-level users.
    """
    data = request.json
    user_role = request.headers.get("X-User-Role")

    if user_role != "admin":
        return jsonify({"error": "Unauthorized — admin access required"}), 403

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    try:
        updated_product = product_update_service.update_product(product_id, data)
        return jsonify({"message": "Product updated successfully", "product": updated_product.dict()}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to update product"}), 500
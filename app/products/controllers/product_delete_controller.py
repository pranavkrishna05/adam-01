"""
Controller for handling product deletion by admin.
"""

from flask import request, jsonify, Blueprint
from products.services.product_delete_service import ProductDeleteService

product_delete_controller = Blueprint("product_delete_controller", __name__)
product_delete_service = ProductDeleteService()


@product_delete_controller.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id: int):
    """
    Endpoint to delete an existing product.
    Requires admin privileges and explicit confirmation.
    """
    user_role = request.headers.get("X-User-Role")
    confirmation = request.args.get("confirm")

    if user_role != "admin":
        return jsonify({"error": "Unauthorized — admin access required"}), 403

    if confirmation != "true":
        return jsonify({"error": "Deletion not confirmed. Set confirm=true to proceed."}), 400

    try:
        product_delete_service.delete_product(product_id)
        return jsonify({"message": "Product deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Failed to delete product"}), 500
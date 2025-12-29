"""
Controller for managing product deletion.
"""

from flask import request, jsonify, Blueprint
from products.services.product_deletion_service import ProductDeletionService

product_deletion_controller = Blueprint("product_deletion_controller", __name__)
product_deletion_service = ProductDeletionService()

@product_deletion_controller.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Endpoint for deleting a product from the catalog.
    Only accessible to admin users.
    """
    admin_token = request.headers.get("Admin-Token")
    confirmation = request.json.get("confirmation")

    if not product_deletion_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    if confirmation != "CONFIRM":
        return jsonify({"error": "Confirmation required to delete the product"}), 400

    success = product_deletion_service.delete_product(product_id)
    if success:
        return jsonify({"message": "Product deleted successfully"}), 200

    return jsonify({"error": "Product not found or could not be deleted"}), 404
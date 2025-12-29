"""
Controller for managing product categories.
"""

from flask import request, jsonify, Blueprint
from products.services.category_service import CategoryService

product_category_controller = Blueprint("product_category_controller", __name__)
category_service = CategoryService()

@product_category_controller.route("/categories", methods=["POST"])
def create_category():
    """
    Endpoint to create a new product category.
    Only accessible to admin users.
    """
    data = request.json
    admin_token = request.headers.get("Admin-Token")

    if not category_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    name = data.get("name")
    parent_id = data.get("parent_id")

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    new_category = category_service.create_category(name, parent_id)
    if new_category:
        return jsonify(new_category.dict()), 201

    return jsonify({"error": "Failed to create category"}), 500


@product_category_controller.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    """
    Endpoint to update an existing category.
    Only accessible to admin users.
    """
    data = request.json
    admin_token = request.headers.get("Admin-Token")

    if not category_service.validate_admin(admin_token):
        return jsonify({"error": "Unauthorized access"}), 403

    name = data.get("name")
    parent_id = data.get("parent_id")

    if not name:
        return jsonify({"error": "Category name is required"}), 400

    updated_category = category_service.update_category(category_id, name, parent_id)
    if updated_category:
        return jsonify(updated_category.dict()), 200

    return jsonify({"error": "Failed to update category or category not found"}), 404


@product_category_controller.route("/categories", methods=["GET"])
def get_all_categories():
    """
    Endpoint to get all categories, including hierarchical categories.
    """
    categories = category_service.get_all_categories()
    return jsonify([category.dict() for category in categories]), 200
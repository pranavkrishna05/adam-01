"""
Controller for managing product categories by admin users.
"""

from flask import request, jsonify, Blueprint
from products.services.category_service import CategoryService

category_controller = Blueprint("category_controller", __name__)
category_service = CategoryService()


@category_controller.route("/categories", methods=["POST"])
def create_category():
    """
    Endpoint to create a new product category.
    Only accessible by admin users.
    """
    data = request.json
    user_role = request.headers.get("X-User-Role")

    if user_role != "admin":
        return jsonify({"error": "Unauthorized — admin access required"}), 403

    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    try:
        category = category_service.create_category(
            name=data["name"],
            parent_id=data.get("parent_id")
        )
        return jsonify({"message": "Category created successfully", "category": category.dict()}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to create category"}), 500


@category_controller.route("/categories", methods=["GET"])
def list_categories():
    """
    Endpoint to list all categories, including hierarchy.
    """
    try:
        categories = category_service.list_categories()
        return jsonify(categories), 200
    except Exception:
        return jsonify({"error": "Failed to retrieve categories"}), 500
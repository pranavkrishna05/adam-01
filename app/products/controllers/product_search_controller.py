"""
Controller for managing product search functionality.
"""

from flask import request, jsonify, Blueprint
from products.services.product_search_service import ProductSearchService

product_search_controller = Blueprint("product_search_controller", __name__)
product_search_service = ProductSearchService()

@product_search_controller.route("/products/search", methods=["GET"])
def search_products():
    """
    Endpoint to search for products in the catalog.
    Supports searching by keywords, categories, and attributes with pagination.
    """
    query = request.args.get("query", "").strip()
    category = request.args.get("category", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    if not query and not category:
        return jsonify({"error": "Query or category is required"}), 400

    search_results = product_search_service.search_products(query, category, page, per_page)
    return jsonify(search_results), 200
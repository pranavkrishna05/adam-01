"""
Controller for handling product search requests.
"""

from flask import request, jsonify, Blueprint
from products.services.product_search_service import ProductSearchService

product_search_controller = Blueprint("product_search_controller", __name__)
product_search_service = ProductSearchService()


@product_search_controller.route("/products/search", methods=["GET"])
def search_products():
    """
    Endpoint to search for products by name, category, or description.
    Returns paginated results with highlighted matched terms.
    """
    query = request.args.get("query", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        results = product_search_service.search_products(query, page, per_page)
        return jsonify(results), 200
    except Exception:
        return jsonify({"error": "Failed to perform search"}), 500
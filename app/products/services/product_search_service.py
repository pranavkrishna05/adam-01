"""
Service for managing product search operations.
"""

from db.database import Database

class ProductSearchService:
    """
    Handles the business logic for searching products in the catalog.
    """

    def __init__(self):
        self.db = Database()

    def search_products(self, query: str, category: str, page: int, per_page: int) -> dict:
        """
        Searches for products in the database based on query and category.
        Supports pagination and returns relevant results.
        """
        filters = {}
        
        if query:
            filters["query"] = query
        if category:
            filters["category"] = category

        # Retrieve products from database based on filters.
        products, total_results = self.db.search_products(filters, page, per_page)

        # Build response with pagination metadata and results.
        results = {
            "total_results": total_results,
            "current_page": page,
            "per_page": per_page,
            "total_pages": (total_results + per_page - 1) // per_page,  # Calculate total pages.
            "products": [
                {
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "description": product["description"],
                    "highlighted_name": self.highlight_query(product["name"], query),
                }
                for product in products
            ],
        }
        return results

    def highlight_query(self, text: str, query: str) -> str:
        """
        Highlights the matching query terms in the text.
        """
        if not query:
            return text

        # Simple highlighting using <strong> tags.
        for term in query.split():
            text = text.replace(term, f"<strong>{term}</strong>")
        return text
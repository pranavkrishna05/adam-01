"""
Service to handle search operations within the product catalog.
"""

import re
from typing import Dict, List, Any
from db.database import Database


class ProductSearchService:
    """
    Handles searching and pagination of product results.
    """

    def __init__(self):
        self.db = Database()

    def search_products(self, query: str, page: int, per_page: int) -> Dict[str, Any]:
        """
        Searches products by name, category, or description.
        Includes pagination and highlights matched terms.
        """
        all_matches = self.db.search_products(query)

        filtered = [p for p in all_matches if not p.get("is_deleted", False) and p.get("active", True)]
        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page
        paged = filtered[start:end]

        highlighted = [self._highlight_fields(p, query) for p in paged]

        return {
            "query": query,
            "total_results": total,
            "page": page,
            "per_page": per_page,
            "results": highlighted,
        }

    def _highlight_fields(self, product: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Adds highlighting tags around matched terms in product fields.
        """
        escaped_query = re.escape(query)
        pattern = re.compile(rf"({escaped_query})", re.IGNORECASE)

        product_copy = product.copy()
        for key in ["name", "description", "category"]:
            if key in product_copy and isinstance(product_copy[key], str):
                product_copy[key] = re.sub(pattern, r"<mark>\1</mark>", product_copy[key])

        return product_copy
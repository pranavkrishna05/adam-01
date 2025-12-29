"""
Service layer handling category management logic.
"""

from typing import Optional, List, Dict
from products.models.category_model import Category
from db.database import Database


class CategoryService:
    """
    Business logic for category creation, retrieval, and hierarchy management.
    """

    def __init__(self):
        self.db = Database()

    def create_category(self, name: str, parent_id: Optional[int] = None) -> Category:
        """
        Creates a category with optional hierarchical parent.
        Ensures unique category names.
        """
        if not name.strip():
            raise ValueError("Category name cannot be empty")

        existing = self.db.get_category_by_name(name)
        if existing:
            raise ValueError("Category name must be unique")

        if parent_id:
            parent = self.db.get_category_by_id(parent_id)
            if not parent:
                raise ValueError("Parent category does not exist")

        new_category_id = self.db.insert_category({"name": name, "parent_id": parent_id})
        saved = self.db.get_category_by_id(new_category_id)
        return Category(**saved)

    def list_categories(self) -> List[Dict]:
        """
        Retrieves all categories and builds a hierarchical structure.
        """
        categories = self.db.get_all_categories()
        category_map = {c["id"]: {"id": c["id"], "name": c["name"], "children": []} for c in categories}

        roots = []
        for c in categories:
            if c["parent_id"]:
                parent = category_map.get(c["parent_id"])
                if parent:
                    parent["children"].append(category_map[c["id"]])
            else:
                roots.append(category_map[c["id"]])
        return roots
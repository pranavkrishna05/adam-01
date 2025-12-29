"""
Service for managing product categories.
"""

from products.models.category_model import Category
from db.database import Database

class CategoryService:
    """
    Handles the business logic for managing product categories.
    """

    ADMIN_SECRET = "super-secret-admin-token"  # Example token for admin authentication.

    def __init__(self):
        self.db = Database()

    def validate_admin(self, token: str) -> bool:
        """
        Validates if the provided token belongs to an authorized admin.
        """
        return token == self.ADMIN_SECRET

    def create_category(self, name: str, parent_id: int | None) -> Category | None:
        """
        Creates a new category in the database.
        """
        category_id = self.db.insert_category({"name": name, "parent_id": parent_id})
        if category_id:
            return Category(id=category_id, name=name, parent_id=parent_id)
        return None

    def update_category(self, category_id: int, name: str, parent_id: int | None) -> Category | None:
        """
        Updates an existing category in the database.
        """
        success = self.db.update_category(category_id, {"name": name, "parent_id": parent_id})
        if success:
            updated_category = self.db.get_category_by_id(category_id)
            return Category(**updated_category)
        return None

    def get_all_categories(self) -> list[Category]:
        """
        Retrieves all categories from the database.
        """
        categories_data = self.db.get_all_categories()
        return [Category(**data) for data in categories_data]
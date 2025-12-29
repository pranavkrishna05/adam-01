"""
Service for managing product updates.
"""

from products.models.product_model import Product
from db.database import Database

class ProductUpdateService:
    """
    Handles validation and updates for existing products.
    """

    ADMIN_SECRET = "super-secret-admin-token"  # Example admin token for validation purposes.

    def __init__(self):
        self.db = Database()

    def validate_admin(self, token: str) -> bool:
        """
        Validates if the provided token belongs to an authorized admin.
        """
        return token == self.ADMIN_SECRET

    def is_duplicate_name(self, product_id: int, name: str) -> bool:
        """
        Checks if the provided name already exists for another product.
        """
        existing_product = self.db.get_product_by_name(name)
        return existing_product and existing_product["id"] != product_id

    def update_product(self, product_id: int, name: str | None, price: float | None, description: str | None, category_id: int | None) -> Product | None:
        """
        Updates product details and returns the updated product.
        """
        update_fields = {}
        if name:
            update_fields["name"] = name
        if price is not None:
            update_fields["price"] = price
        if description is not None:
            update_fields["description"] = description
        if category_id is not None:
            update_fields["category_id"] = category_id

        success = self.db.update_product(product_id, update_fields)
        if success:
            product_data = self.db.get_product_by_id(product_id)
            return Product(**product_data)
        return None
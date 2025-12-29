"""
Service for managing updates to existing product details.
"""

from products.models.product_model import Product
from db.database import Database

class ProductUpdateService:
    """
    Handles the business logic for updating product details.
    """

    ADMIN_SECRET = "super-secret-admin-token"  # Example token for admin authentication.

    def __init__(self):
        self.db = Database()

    def validate_admin(self, token: str) -> bool:
        """
        Validates if the provided token belongs to an authorized admin.
        """
        return token == self.ADMIN_SECRET

    def is_product_name_exists(self, product_id: int, name: str) -> bool:
        """
        Checks if another product with the given name already exists.
        """
        existing_product = self.db.get_product_by_name(name)
        return existing_product is not None and existing_product.get("id") != product_id

    def is_valid_price(self, price: float) -> bool:
        """
        Validates if the product price is a positive number.
        """
        return isinstance(price, (int, float)) and price > 0

    def update_product(self, product_id: int, name: str | None, price: float | None, description: str | None) -> Product | None:
        """
        Updates the product details in the database.
        """
        update_fields = {}
        if name:
            update_fields["name"] = name
        if price is not None:
            update_fields["price"] = price
        if description is not None:
            update_fields["description"] = description

        success = self.db.update_product(product_id, update_fields)
        if success:
            updated_product = self.db.get_product_by_id(product_id)
            return Product(**updated_product)
        return None
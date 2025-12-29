"""
Service for managing the creation of new products.
"""

from products.models.product_model import Product
from db.database import Database

class ProductCreationService:
    """
    Handles the business logic for creating new products in the inventory.
    """

    ADMIN_SECRET = "super-secret-admin-token"  # Example token for admin authentication.

    def __init__(self):
        self.db = Database()

    def validate_admin(self, token: str) -> bool:
        """
        Validates if the provided token belongs to an authorized admin.
        """
        return token == self.ADMIN_SECRET

    def is_product_name_exists(self, name: str) -> bool:
        """
        Checks if a product with the given name already exists.
        """
        existing_product = self.db.get_product_by_name(name)
        return existing_product is not None

    def is_valid_price(self, price: float) -> bool:
        """
        Validates if the product price is a positive number.
        """
        return isinstance(price, (int, float)) and price > 0

    def create_product(self, name: str, price: float, description: str, category_id: int | None) -> Product | None:
        """
        Creates a new product and adds it to the database.
        """
        product_data = {
            "name": name,
            "price": price,
            "description": description,
            "category_id": category_id,
        }
        product_id = self.db.insert_product(product_data)
        if product_id:
            product_data["id"] = product_id
            return Product(**product_data)
        return None
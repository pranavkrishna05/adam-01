"""
Service for managing product-related logic.
"""

from products.models.product_model import Product
from db.database import Database

class ProductService:
    """
    Handles validation, creation, retrieval, and updates for products.
    """

    ADMIN_SECRET = "super-secret-admin-token"  # Example admin token for validation purposes.

    def __init__(self):
        self.db = Database()

    def validate_admin(self, token: str) -> bool:
        """
        Validates if the provided token belongs to an authorized admin.
        """
        return token == self.ADMIN_SECRET

    def create_product(self, name: str, price: float, description: str, category_id: int | None) -> Product | None:
        """
        Creates a new product if the name is unique.
        """
        existing_product = self.db.get_product_by_name(name)

        if existing_product:
            return None

        product_data = {
            "name": name,
            "price": price,
            "description": description,
            "category_id": category_id,
        }
        product_id = self.db.insert_product(product_data)
        return Product(id=product_id, **product_data)

    def get_all_products(self) -> list[Product]:
        """
        Retrieves all products from the inventory.
        """
        product_records = self.db.get_all_products()
        return [Product(**record) for record in product_records]
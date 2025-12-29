"""
Service layer handling product management logic.
"""

from products.models.product_model import Product
from db.database import Database
from datetime import datetime


class ProductService:
    """
    Business logic service for creating and managing products.
    """

    def __init__(self):
        self.db = Database()

    def create_product(self, name: str, price: float, description: str, category: str) -> Product:
        """
        Creates a new product with validation for unique name and valid data.
        """
        if not name.strip():
            raise ValueError("Product name cannot be empty")

        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Product price must be a positive number")

        if not description.strip():
            raise ValueError("Product description cannot be empty")

        existing = self.db.get_product_by_name(name)
        if existing:
            raise ValueError("Product name must be unique")

        product_data = {
            "name": name,
            "price": price,
            "description": description,
            "category": category,
            "created_at": datetime.utcnow().isoformat(),
        }

        new_product_id = self.db.insert_product(product_data)
        return Product(id=new_product_id, **product_data)
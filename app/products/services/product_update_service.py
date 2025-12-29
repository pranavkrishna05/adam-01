"""
Service layer to handle admin-based product update logic.
"""

from products.models.product_model import Product
from db.database import Database


class ProductUpdateService:
    """
    Implements business logic for updating existing products.
    """

    def __init__(self):
        self.db = Database()

    def update_product(self, product_id: int, updates: dict) -> Product:
        """
        Updates an existing product’s details with validation.
        """

        existing_product = self.db.get_product_by_id(product_id)
        if not existing_product:
            raise ValueError("Product not found")

        new_data = {}

        # Validate name if being updated
        if "name" in updates:
            new_name = updates["name"].strip()
            if not new_name:
                raise ValueError("Product name cannot be empty")
            if new_name != existing_product["name"]:
                name_conflict = self.db.get_product_by_name(new_name)
                if name_conflict and name_conflict["id"] != product_id:
                    raise ValueError("Product name must be unique")
            new_data["name"] = new_name

        # Validate price input
        if "price" in updates:
            price = updates["price"]
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("Price must be a numeric value greater than 0")
            new_data["price"] = price

        # Validate description — cannot be empty or removed entirely
        if "description" in updates:
            desc = updates["description"]
            if not desc or not desc.strip():
                raise ValueError("Product description cannot be removed or empty")
            new_data["description"] = desc.strip()

        # Category can be modified if provided
        if "category" in updates:
            category = updates["category"].strip()
            if not category:
                raise ValueError("Category cannot be empty")
            new_data["category"] = category

        # Update the product in DB
        updated_record = self.db.update_product(product_id, new_data)
        return Product(**updated_record)
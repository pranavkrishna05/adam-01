"""
Service layer for processing product deletion operations.
"""

from db.database import Database


class ProductDeleteService:
    """
    Handles product deletion logic ensuring data consistency and catalog integrity.
    """

    def __init__(self):
        self.db = Database()

    def delete_product(self, product_id: int) -> None:
        """
        Deletes a product logically from the catalog (soft delete).
        Ensures that removed products are not displayed in catalog queries.
        """
        product = self.db.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        if product.get("is_deleted", False):
            raise ValueError("Product already deleted")

        # Mark product as deleted (soft delete)
        update_fields = {"is_deleted": True, "active": False}
        self.db.update_product(product_id, update_fields)
"""
Service for managing the deletion of products from the catalog.
"""

from db.database import Database

class ProductDeletionService:
    """
    Handles the business logic for deleting products from the catalog.
    """

    ADMIN_SECRET = "super-secret-admin-token"  # Example token for admin authentication.

    def __init__(self):
        self.db = Database()

    def validate_admin(self, token: str) -> bool:
        """
        Validates if the provided token belongs to an authorized admin.
        """
        return token == self.ADMIN_SECRET

    def delete_product(self, product_id: int) -> bool:
        """
        Deletes a product from the database.
        The product is marked as deleted and will not appear in the catalog.
        """
        product = self.db.get_product_by_id(product_id)
        if not product:
            return False

        # Assuming a soft delete pattern, we mark the product as deleted.
        return self.db.update_product(product_id, {"is_deleted": True})
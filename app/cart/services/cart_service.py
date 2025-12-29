"""
Service for managing shopping cart operations.
"""

from cart.models.cart_model import Cart
from db.database import Database

class CartService:
    """
    Handles the business logic for shopping cart operations.
    """

    def __init__(self):
        self.db = Database()

    def get_cart(self, user_id: str) -> dict:
        """
        Retrieves the shopping cart for the given user.
        """
        cart_data = self.db.get_cart_by_user_id(user_id)
        if not cart_data:
            return {"products": [], "total_price": 0.0}
        
        return {
            "products": cart_data["products"],
            "total_price": cart_data["total_price"],
        }

    def add_to_cart(self, user_id: str, product_id: int, quantity: int) -> bool:
        """
        Adds a product to the user's shopping cart.
        """
        product = self.db.get_product_by_id(product_id)
        if not product:
            return False

        return self.db.add_to_cart(user_id, {"product_id": product_id, "quantity": quantity})

    def remove_from_cart(self, user_id: str, product_id: int) -> bool:
        """
        Removes a product from the user's shopping cart.
        """
        return self.db.remove_from_cart(user_id, product_id)
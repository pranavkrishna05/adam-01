"""
Service to handle the removal of items from the shopping cart.
"""

from db.database import Database
from cart.models.cart_model import Cart

class CartItemService:
    """
    Handles the business logic of removing items from the shopping cart.
    """

    def __init__(self):
        self.db = Database()

    def remove_item(self, user_id: str, product_id: int) -> bool:
        """
        Removes the specified product from the user's shopping cart
        and updates the total price.
        """
        # Check if the product exists in the user's cart
        cart = self.db.get_cart_by_user_id(user_id)
        if not cart or product_id not in [item["product_id"] for item in cart["products"]]:
            return False

        # Remove the product from the database and update total price
        success = self.db.remove_from_cart(user_id, product_id)
        if success:
            self._update_total_price(user_id)
        return success

    def _update_total_price(self, user_id: str):
        """
        Recalculates the total price for the user's cart.
        """
        cart_data = self.db.get_cart_by_user_id(user_id)
        if cart_data:
            total_price = sum(
                item["quantity"] * self.db.get_product_by_id(item["product_id"])["price"]
                for item in cart_data["products"]
            )
            self.db.update_cart_total_price(user_id, total_price)
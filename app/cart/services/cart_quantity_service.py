"""
Service to handle product quantity modifications in the shopping cart.
"""

from db.database import Database
from cart.models.cart_model import Cart

class CartQuantityService:
    """
    Handles the business logic for modifying product quantities in the shopping cart.
    """

    def __init__(self):
        self.db = Database()

    def update_quantity(self, user_id: str, product_id: int, quantity: int) -> bool:
        """
        Updates the quantity of a product in the user's shopping cart
        and recalculates the total price.
        """
        # Check if the product exists in the user's cart
        cart = self.db.get_cart_by_user_id(user_id)
        if not cart or product_id not in [item["product_id"] for item in cart["products"]]:
            return False

        # Update product quantity in the cart
        success = self.db.update_cart_item(user_id, product_id, {"quantity": quantity})
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
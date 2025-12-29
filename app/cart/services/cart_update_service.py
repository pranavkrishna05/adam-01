"""
Service layer responsible for updating product quantities in the shopping cart.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from db.database import Database


class CartUpdateService:
    """
    Handles quantity modifications and corresponding price recalculations.
    """

    def __init__(self):
        self.db = Database()

    def update_quantity(
        self,
        product_id: int,
        quantity: int,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> Dict[str, Any]:
        """
        Updates the quantity of a product in a user's or guest's cart.
        Recalculates total price upon successful update.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if user_id:
            cart_item = self.db.get_cart_item_by_user(user_id, product_id)
        else:
            cart_item = self.db.get_cart_item_by_session(session_id, product_id)

        if not cart_item:
            raise ValueError("Product not found in cart")

        product = self.db.get_product_by_id(product_id)
        if not product or not product.get("active", True) or product.get("is_deleted", False):
            raise ValueError("Product not available")

        # Update the cart item with the new quantity
        self.db.update_cart_item(
            cart_item["id"],
            {"quantity": quantity, "updated_at": datetime.utcnow()},
        )

        return self._recalculate_total(user_id=user_id, session_id=session_id)

    def _recalculate_total(
        self, user_id: Optional[str], session_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Recomputes the cart's total price and metadata after any update.
        """
        if user_id:
            items = self.db.get_cart_items_by_user(user_id)
        else:
            items = self.db.get_cart_items_by_session(session_id)

        total_price = 0.0
        for item in items:
            product = self.db.get_product_by_id(item["product_id"])
            if product and product.get("active", True) and not product.get("is_deleted", False):
                total_price += product["price"] * item["quantity"]

        return {
            "items": items,
            "summary": {
                "item_count": len(items),
                "total_price": round(total_price, 2),
                "updated_at": datetime.utcnow(),
            },
        }
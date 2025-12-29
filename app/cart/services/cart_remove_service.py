"""
Service layer for handling product removal from shopping cart.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from db.database import Database


class CartRemoveService:
    """
    Handles item removal, confirmation enforcement, and cart total price recalculation.
    """

    def __init__(self):
        self.db = Database()

    def remove_item(
        self, product_id: int,
        user_id: Optional[str],
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Removes an item from the cart and updates cart totals.
        Raises ValueError if item not found or already deleted.
        """
        if user_id:
            cart_item = self.db.get_cart_item_by_user(user_id, product_id)
        else:
            cart_item = self.db.get_cart_item_by_session(session_id, product_id)

        if not cart_item:
            raise ValueError("Product not found in cart")

        self.db.delete_cart_item(cart_item["id"])

        return self._recalculate_cart_total(user_id=user_id, session_id=session_id)

    def _recalculate_cart_total(self, user_id: Optional[str], session_id: Optional[str]) -> Dict[str, Any]:
        """
        Recalculates the total price of cart after modifications.
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

        metadata = {
            "updated_at": datetime.utcnow(),
            "item_count": len(items),
            "total_price": round(total_price, 2)
        }
        return {"items": items, "summary": metadata}
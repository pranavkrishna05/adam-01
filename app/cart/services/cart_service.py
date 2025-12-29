"""
Service layer for shopping cart logic.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from db.database import Database
from cart.models.cart_model import CartItem


class CartService:
    """
    Manages adding, removing, and viewing cart items
    for users and guest sessions.
    """

    def __init__(self):
        self.db = Database()

    def get_cart(self, user_id: Optional[str], session_id: Optional[str]) -> Dict[str, Any]:
        """
        Fetches cart contents for a user or a guest session.
        """
        if user_id:
            cart_items = self.db.get_cart_items_by_user(user_id)
        else:
            cart_items = self.db.get_cart_items_by_session(session_id)

        return {"items": cart_items, "item_count": len(cart_items)}

    def add_to_cart(
        self,
        product_id: int,
        quantity: int,
        user_id: Optional[str],
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Adds or increments a product in the user's shopping cart.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1")

        product = self.db.get_product_by_id(product_id)
        if not product or product.get("is_deleted", False) or not product.get("active", True):
            raise ValueError("Product not available")

        if user_id:
            existing = self.db.get_cart_item_by_user(user_id, product_id)
        else:
            existing = self.db.get_cart_item_by_session(session_id, product_id)

        if existing:
            new_quantity = existing["quantity"] + quantity
            self.db.update_cart_item(existing["id"], {"quantity": new_quantity, "updated_at": datetime.utcnow()})
        else:
            cart_item = {
                "product_id": product_id,
                "quantity": quantity,
                "user_id": user_id,
                "session_id": session_id,
                "added_at": datetime.utcnow(),
            }
            self.db.insert_cart_item(cart_item)

        return self.get_cart(user_id, session_id)

    def remove_from_cart(
        self,
        product_id: int,
        user_id: Optional[str],
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Removes a product from the user's cart.
        """
        if user_id:
            existing = self.db.get_cart_item_by_user(user_id, product_id)
        else:
            existing = self.db.get_cart_item_by_session(session_id, product_id)

        if not existing:
            raise ValueError("Product not found in cart")

        self.db.delete_cart_item(existing["id"])
        return self.get_cart(user_id, session_id)
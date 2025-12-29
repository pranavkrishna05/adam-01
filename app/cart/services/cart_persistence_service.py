"""
Service responsible for persisting a user's shopping cart across sessions.
"""

from datetime import datetime
from typing import Dict, Optional, Any
from db.database import Database


class CartPersistenceService:
    """
    Handles cart state storage and retrieval linked to user profiles.
    """

    def __init__(self):
        self.db = Database()

    def save_cart_state(self, user_id: str) -> Dict[str, Any]:
        """
        Saves the current state of the user's cart into their user profile.
        """
        cart_items = self.db.get_cart_items_by_user(user_id)
        if not cart_items:
            raise ValueError("No items in cart to save")

        total_price = 0.0
        for item in cart_items:
            product = self.db.get_product_by_id(item["product_id"])
            if product and product.get("active", True) and not product.get("is_deleted", False):
                total_price += product["price"] * item["quantity"]

        saved_state = {
            "items": cart_items,
            "total_price": round(total_price, 2),
            "saved_at": datetime.utcnow(),
        }

        self.db.update_user_profile(user_id, {"saved_cart": saved_state})
        return saved_state

    def load_cart_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the previously saved cart state for the user.
        Recreates persisted items into the user's active cart if available.
        """
        user_profile = self.db.get_user_profile(user_id)
        if not user_profile or "saved_cart" not in user_profile:
            return None

        saved_cart = user_profile["saved_cart"]
        if not saved_cart.get("items"):
            return None

        # Clear current active cart before restoring (avoiding duplicates)
        self.db.clear_cart_for_user(user_id)

        # Reinsert saved cart items
        for item in saved_cart["items"]:
            self.db.insert_cart_item({
                "user_id": user_id,
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "added_at": datetime.utcnow(),
            })

        # Recalculate prices to ensure consistency with current product data
        return self._recalculate_cart(user_id)

    def _recalculate_cart(self, user_id: str) -> Dict[str, Any]:
        """
        Recomputes cart details after reloading from persistence.
        """
        items = self.db.get_cart_items_by_user(user_id)
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
                "restored_at": datetime.utcnow(),
            },
        }
"""
Model representing a persisted shopping cart linked to a user profile.
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from cart.models.cart_model import CartItem


class SavedCart(BaseModel):
    items: List[CartItem]
    total_price: float = Field(..., ge=0)
    saved_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
```
"""
Cart models representing a shopping cart item and the complete cart state.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity of the product in cart")
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Cart(BaseModel):
    items: List[CartItem]
    item_count: int
    total_price: float = Field(..., ge=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
```
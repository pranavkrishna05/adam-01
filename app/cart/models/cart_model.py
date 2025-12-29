"""
Cart model representing items and total metadata for user or session.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int = Field(..., gt=0)
    user_id: Optional[str]
    session_id: Optional[str]
    added_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class Cart(BaseModel):
    items: List[CartItem]
    item_count: int = 0
    total_price: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
```
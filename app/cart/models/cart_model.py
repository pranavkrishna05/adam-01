"""
Data model representing a shopping cart item.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int = Field(..., gt=0)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
```
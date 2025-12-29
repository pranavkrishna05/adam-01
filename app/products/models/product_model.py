"""
Product model representing catalog items and state.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    active: bool = True
```
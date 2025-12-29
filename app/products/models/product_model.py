"""
Product model definition representing items in the inventory.
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
    created_at: Optional[datetime]
```
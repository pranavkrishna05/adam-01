"""
Model representing a product category with hierarchy support.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Category(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[int] = None
    children: List["Category"] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
```
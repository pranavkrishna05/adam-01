"""
Category model definition for representing product categories.
"""

from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
```
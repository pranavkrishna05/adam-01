"""
Product model definition for representing inventory items.
"""

from pydantic import BaseModel

class Product(BaseModel):
    id: int | None
    name: str
    price: float
    description: str
    category_id: int | None
```
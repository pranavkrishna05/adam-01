"""
Cart model definition for representing the shopping cart.
"""

from pydantic import BaseModel
from typing import List, Dict

class Cart(BaseModel):
    user_id: str
    products: List[Dict]  # Each product is represented as {"product_id": int, "quantity": int}
    total_price: float
```
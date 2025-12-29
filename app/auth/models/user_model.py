"""
User model definition for account management representation.
"""

from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    email: str
    password: str
```
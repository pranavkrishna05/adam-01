"""
User profile model definition for account customization.
"""

from pydantic import BaseModel

class UserProfile(BaseModel):
    id: int | None
    email: str
    name: str | None
    phone: str | None
    preferences: dict | None
```
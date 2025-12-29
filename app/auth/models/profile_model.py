"""
Profile model definition representing user personal information and preferences.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict

class Profile(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    preferences: Optional[Dict[str, str]] = None
```
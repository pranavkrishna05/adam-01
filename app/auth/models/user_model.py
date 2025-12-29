"""
User model definition for representing registered users.
"""

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
```
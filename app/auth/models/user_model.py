"""
User model definition representing registered platform users.
"""

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
```
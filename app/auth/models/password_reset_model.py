"""
Password Reset model for handling reset token storage and validation.
"""

from pydantic import BaseModel

class PasswordReset(BaseModel):
    id: int | None
    email: str
    token: str
    expires_at: int
```
"""
Password reset token model for representing the reset process.
"""

from pydantic import BaseModel
from datetime import datetime

class PasswordResetToken(BaseModel):
    email: str
    token: str
    expires_at: datetime
```
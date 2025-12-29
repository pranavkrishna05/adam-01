"""
Session model definition for managing user sessions.
"""

from pydantic import BaseModel

class Session(BaseModel):
    id: int | None
    email: str
    session_token: str
    created_at: int
```
"""
Service for managing user authentication and session handling.
"""

import hashlib
import time
import jwt
from db.database import Database

class LoginService:
    """
    Handles user authentication and session token generation.
    """

    SECRET_KEY = "super-secret-key"
    TOKEN_EXPIRATION = 3600  # Session tokens expire after 1 hour.
    MAX_INVALID_ATTEMPTS = 5

    def __init__(self):
        self.db = Database()
        self.invalid_attempts = {}

    def authenticate_user(self, email: str, password: str) -> str | None:
        """
        Authenticates user credentials and returns a session token if successful.
        """
        user_record = self.db.get_user_by_email(email)
        if not user_record:
            self.record_invalid_attempt(email)
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password != user_record["password"]:
            self.record_invalid_attempt(email)
            return None

        if self.invalid_attempts.get(email, 0) >= self.MAX_INVALID_ATTEMPTS:
            return None

        return self.generate_token(email)

    def generate_token(self, email: str) -> str:
        """
        Generates a session token with expiration metadata.
        """
        payload = {
            "email": email,
            "exp": int(time.time()) + self.TOKEN_EXPIRATION
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def record_invalid_attempt(self, email: str) -> None:
        """
        Records invalid login attempts and enforces limits.
        """
        if email not in self.invalid_attempts:
            self.invalid_attempts[email] = 0
        self.invalid_attempts[email] += 1

        # Optionally, handle locking out the user after too many attempts.
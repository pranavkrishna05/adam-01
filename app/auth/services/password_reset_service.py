"""
Service for managing password reset requests and token validation.
"""

import hashlib
import uuid
import time
from db.database import Database

class PasswordResetService:
    """
    Handles password reset logic, including token generation, expiration, and validation.
    """

    PASSWORD_MIN_LENGTH = 8
    TOKEN_EXPIRATION_SECONDS = 86400  # Reset tokens expire after 24 hours.

    def __init__(self):
        self.db = Database()

    def is_password_secure(self, password: str) -> bool:
        """
        Checks if the password meets security criteria.
        Criteria: minimum length and complexity.
        """
        return len(password) >= self.PASSWORD_MIN_LENGTH and any(char.isdigit() for char in password)

    def send_reset_link(self, email: str) -> bool:
        """
        Sends a password reset link to the provided email.
        Generates a unique reset token and stores it with an expiration timestamp.
        """
        user_record = self.db.get_user_by_email(email)
        if not user_record:
            return False

        reset_token = str(uuid.uuid4())
        expiration = int(time.time()) + self.TOKEN_EXPIRATION_SECONDS
        self.db.insert_password_reset({"email": email, "token": reset_token, "expires_at": expiration})

        # Replace with actual email sending logic.
        print(f"Password reset link: http://example.com/password-reset/{reset_token}")  # Example.
        return True

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Resets the password if the token is valid and has not expired.
        """
        reset_record = self.db.get_password_reset_by_token(token)
        if not reset_record or reset_record["expires_at"] < int(time.time()):
            return False

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        self.db.update_user_password(reset_record["email"], hashed_password)
        self.db.delete_password_reset(token)
        return True
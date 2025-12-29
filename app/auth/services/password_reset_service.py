"""
Service to handle secure password reset functionality.
"""

import secrets
import re
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from db.database import Database
from auth.models.user_model import User

class PasswordResetService:
    """
    Handles password reset requests, email verification, and token-based reset flow.
    """

    TOKEN_EXPIRATION_HOURS = 24

    def __init__(self):
        self.db = Database()

    def initiate_reset(self, email: str) -> None:
        """
        Initiates password reset process by generating a reset token and sending it to the user.
        """
        user = self.db.get_user_by_email(email)
        if not user:
            raise ValueError("No user found with this email")

        token = secrets.token_urlsafe(32)
        expiration_time = datetime.utcnow() + timedelta(hours=self.TOKEN_EXPIRATION_HOURS)
        self.db.save_password_reset_token(email, token, expiration_time)
        self._send_reset_email(email, token)

    def reset_password(self, token: str, new_password: str) -> None:
        """
        Resets the user's password if the token is valid and not expired.
        """
        token_record = self.db.get_reset_token_details(token)
        if not token_record:
            raise ValueError("Invalid or expired token")

        if datetime.utcnow() > token_record["expires_at"]:
            raise ValueError("Reset token has expired")

        if not self._is_secure_password(new_password):
            raise ValueError(
                "Password must be at least 8 characters long, and contain uppercase, lowercase, number, and special character"
            )

        # Hash and update the new password
        hashed_password = generate_password_hash(new_password)
        self.db.update_user_password(token_record["email"], hashed_password)
        self.db.invalidate_reset_token(token)

    def _is_secure_password(self, password: str) -> bool:
        """
        Validates password security against complexity rules.
        """
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        return bool(re.match(pattern, password))

    def _send_reset_email(self, email: str, token: str):
        """
        Simulates sending a password reset email with a secure token-based link.
        In production, integrate with an email delivery service.
        """
        reset_link = f"https://example.com/reset-password?token={token}"
        # Simulated log (normally you'd send via SMTP or external provider)
        print(f"[EMAIL SENT] To: {email} | Reset Link: {reset_link}")
"""
Service for managing password reset requests and processing.
"""

import hashlib
import time
import jwt
import smtplib
from email.message import EmailMessage
from db.database import Database

class PasswordResetService:
    """
    Handles sending password reset links and resetting passwords.
    """

    SECRET_KEY = "super-secret-key"
    TOKEN_EXPIRATION = 86400  # 24 hours in seconds.

    def __init__(self):
        self.db = Database()

    def send_reset_email(self, email: str) -> bool:
        """
        Sends a password reset email with a token if the user exists.
        """
        user_record = self.db.get_user_by_email(email)
        if not user_record:
            return False

        reset_token = self.generate_token(email)
        reset_link = f"https://example.com/password-reset?token={reset_token}"

        # Send the email (assuming SMTP server is configured).
        email_sent = self.send_email(
            recipient=email,
            subject="Password Reset Request",
            body=f"Click the link below to reset your password:\n\n{reset_link}\n\nThis link will expire in 24 hours."
        )
        return email_sent

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Resets the user's password if the token is valid and not expired.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            email = payload.get("email")

            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            success = self.db.update_user_password(email, hashed_password)
            return success
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def generate_token(self, email: str) -> str:
        """
        Generates a reset token with a 24-hour expiration.
        """
        payload = {
            "email": email,
            "exp": int(time.time()) + self.TOKEN_EXPIRATION
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def is_password_secure(self, password: str) -> bool:
        """
        Validates if the password meets the security criteria.
        Criteria: minimum length and complexity (contains at least one digit).
        """
        PASSWORD_MIN_LENGTH = 8
        return len(password) >= PASSWORD_MIN_LENGTH and any(char.isdigit() for char in password)

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Sends an email using an SMTP server.
        """
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = "no-reply@example.com"
            msg["To"] = recipient

            # Example SMTP configuration.
            with smtplib.SMTP("smtp.example.com", 587) as smtp:
                smtp.starttls()
                smtp.login("your-username", "your-password")
                smtp.send_message(msg)
            return True
        except Exception as e:
            # Log the exception in a real application.
            print(f"Failed to send email: {e}")
            return False
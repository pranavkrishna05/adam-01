"""
Service responsible for user authentication and login restrictions.
"""

from werkzeug.security import check_password_hash
from auth.models.user_model import User
from db.database import Database
from datetime import datetime, timedelta

class LoginService:
    """
    Handles user login, authentication, and invalid login attempt control.
    """

    MAX_ATTEMPTS = 5
    LOCKOUT_TIME_MINUTES = 15

    def __init__(self):
        self.db = Database()

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticates a user by verifying email and password.
        Limits invalid login attempts and manages lockout period.
        """
        user_data = self.db.get_user_by_email(email)
        if not user_data:
            raise ValueError("User not found")

        login_attempts = self.db.get_login_attempts(email)
        if login_attempts and login_attempts["count"] >= self.MAX_ATTEMPTS:
            last_attempt_time = login_attempts["last_attempt"]
            if datetime.utcnow() - last_attempt_time < timedelta(minutes=self.LOCKOUT_TIME_MINUTES):
                raise ValueError("Account locked due to multiple invalid login attempts. Try again later.")
            else:
                self.db.reset_login_attempts(email)

        if not check_password_hash(user_data["password"], password):
            self.db.increment_login_attempt(email)
            raise ValueError("Invalid email or password")

        self.db.reset_login_attempts(email)
        return User(id=user_data["id"], email=user_data["email"])
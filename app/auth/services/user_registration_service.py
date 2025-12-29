"""
Service for handling user registration logic.
"""

from auth.models.user_model import User
from db.database import Database
import hashlib

class UserRegistrationService:
    """
    Handles validation, creation, and logic for user registration.
    """

    PASSWORD_MIN_LENGTH = 8

    def __init__(self):
        self.db = Database()

    def is_password_secure(self, password: str) -> bool:
        """
        Checks if the password meets the security criteria.
        Criteria: minimum length and complexity.
        """
        return len(password) >= self.PASSWORD_MIN_LENGTH and any(char.isdigit() for char in password)

    def is_email_taken(self, email: str) -> bool:
        """
        Checks if the email is already registered.
        """
        return self.db.get_user_by_email(email) is not None

    def create_user(self, email: str, password: str) -> User:
        """
        Creates a new user with hashed password.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = {"email": email, "password": hashed_password}
        user_id = self.db.insert_user(user_data)
        return User(id=user_id, **user_data)
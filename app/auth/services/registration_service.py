"""
Service for handling user registration and validation logic.
"""

import hashlib
from auth.models.user_model import User
from db.database import Database

class RegistrationService:
    """
    Service to manage user registration logic and password validation.
    """

    PASSWORD_MIN_LENGTH = 8

    def __init__(self):
        self.db = Database()

    def is_password_secure(self, password: str) -> bool:
        """
        Validates if the password meets the security criteria.
        Criteria: minimum length and complexity (contains at least one digit).
        """
        return len(password) >= self.PASSWORD_MIN_LENGTH and any(char.isdigit() for char in password)

    def create_user(self, email: str, password: str) -> User | None:
        """
        Creates a new user if the email is unique.
        """
        existing_user = self.db.get_user_by_email(email)
        if existing_user:
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = {"email": email, "password": hashed_password}
        user_id = self.db.insert_user(user_data)
        return User(id=user_id, email=email)
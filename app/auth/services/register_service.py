"""
Service responsible for handling user registration logic.
"""

import re
from werkzeug.security import generate_password_hash
from auth.models.user_model import User
from db.database import Database

class RegisterService:
    """
    Handles business logic for user registration.
    """

    def __init__(self):
        self.db = Database()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with a unique email and secure password.
        Raises ValueError if validation fails.
        """
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        if not self._is_secure_password(password):
            raise ValueError(
                "Password must be at least 8 characters long, and contain uppercase, lowercase, number, and special character"
            )

        if self.db.get_user_by_email(email):
            raise ValueError("Email already exists")

        hashed_password = generate_password_hash(password)
        user_id = self.db.insert_user({"email": email, "password": hashed_password})

        return User(id=user_id, email=email)

    def _is_valid_email(self, email: str) -> bool:
        """
        Validates email format.
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))

    def _is_secure_password(self, password: str) -> bool:
        """
        Ensures password meets security criteria.
        """
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        return bool(re.match(pattern, password))
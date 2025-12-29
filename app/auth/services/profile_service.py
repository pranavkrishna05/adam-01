"""
Service to handle user profile management and updates.
"""

from auth.models.profile_model import Profile
from db.database import Database

class ProfileService:
    """
    Handles the business logic for retrieving and updating user profile data.
    """

    def __init__(self):
        self.db = Database()

    def get_profile(self, user_id: int) -> Profile:
        """
        Fetch user profile details from the database.
        """
        user_record = self.db.get_user_by_id(user_id)
        if not user_record:
            raise ValueError("User not found")

        return Profile(**user_record)

    def update_profile(self, user_id: int, updates: dict) -> Profile:
        """
        Update user profile details and ensure immediate reflection.
        """
        user_record = self.db.get_user_by_id(user_id)
        if not user_record:
            raise ValueError("User not found")

        allowed_fields = {"name", "email", "phone", "address", "preferences"}
        update_data = {key: value for key, value in updates.items() if key in allowed_fields}

        if "email" in update_data:
            existing = self.db.get_user_by_email(update_data["email"])
            if existing and existing["id"] != user_id:
                raise ValueError("Email already in use by another user")

        updated = self.db.update_user_profile(user_id, update_data)
        return Profile(**updated)
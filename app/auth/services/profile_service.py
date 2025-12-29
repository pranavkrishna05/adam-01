"""
Service for managing user profile updates and retrieval.
"""

from auth.models.user_model import User
from db.database import Database

class ProfileService:
    """
    Handles business logic for managing user profiles.
    """

    def __init__(self):
        self.db = Database()

    def get_user_profile(self, user_id: int) -> User | None:
        """
        Retrieves the profile information for a specific user.
        """
        user_record = self.db.get_user_by_id(user_id)
        if not user_record:
            return None
        return User(**user_record)

    def update_user_profile(self, user_id: int, name: str | None, preferences: dict | None) -> User | None:
        """
        Updates the user's profile information.
        """
        update_fields = {}
        if name:
            update_fields["name"] = name
        if preferences:
            update_fields["preferences"] = preferences

        success = self.db.update_user(user_id, update_fields)
        if success:
            user_record = self.db.get_user_by_id(user_id)
            return User(**user_record)
        return None
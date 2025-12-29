"""
Service for managing user profile functionality.
"""

from auth.models.user_profile_model import UserProfile
from db.database import Database

class UserProfileService:
    """
    Service to handle retrieval and updates to user profiles.
    """

    def __init__(self):
        self.db = Database()

    def get_user_profile(self, email: str) -> UserProfile | None:
        """
        Retrieves the profile for the given email.
        """
        profile_data = self.db.get_user_profile_by_email(email)
        if profile_data:
            return UserProfile(**profile_data)
        return None

    def update_user_profile(self, email: str, updates: dict) -> UserProfile | None:
        """
        Updates the profile for the given email.
        """
        success = self.db.update_user_profile(email, updates)
        if success:
            updated_data = self.db.get_user_profile_by_email(email)
            return UserProfile(**updated_data)
        return None
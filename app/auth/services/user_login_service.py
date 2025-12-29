"""
Service for managing user login and session control.
"""

import hashlib
import time
import uuid
from db.database import Database

class UserLoginService:
    """
    Handles user authentication and session management.
    """

    MAX_LOGIN_ATTEMPTS = 5
    SESSION_TIMEOUT_SECONDS = 3600  # Default session timeout is 1 hour.

    def __init__(self):
        self.db = Database()
        self.failed_login_attempts = {}

    def authenticate_user(self, email: str, password: str) -> str | None:
        """
        Authenticates the user's credentials and creates a session if valid.
        Returns session token if successful, or None if authentication fails.
        """
        user_record = self.db.get_user_by_email(email)

        if not user_record:
            self._record_failed_attempt(email)
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user_record["password"] != hashed_password:
            self._record_failed_attempt(email)
            return None

        if self.failed_login_attempts.get(email, 0) >= self.MAX_LOGIN_ATTEMPTS:
            return None

        session_token = self._create_session_token(email)
        self.db.insert_session({"email": email, "session_token": session_token, "created_at": int(time.time())})
        return session_token

    def _record_failed_attempt(self, email: str):
        """
        Records a failed login attempt for the email.
        """
        if email in self.failed_login_attempts:
            self.failed_login_attempts[email] += 1
        else:
            self.failed_login_attempts[email] = 1

    def _create_session_token(self, email: str) -> str:
        """
        Creates a unique session token.
        """
        return str(uuid.uuid4())
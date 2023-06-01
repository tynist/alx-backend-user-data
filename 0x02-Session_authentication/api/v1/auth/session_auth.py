#!/usr/bin/env python3
"""
Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    Manages user sessions and gives authentication functionality
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user ID.
        Args:
            user_id: The ID of the user to create a session for.
        Returns:
            The generated session ID.
        """
        if user_id is None or type(user_id) is not str:
            return None

        ID = str(uuid4())
        self.user_id_by_session_id[ID] = user_id
        return ID


    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.
        Args:
            session_id: The session ID to look up.
        Returns:
            The associated user ID, or None if not found.
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on a session ID.
        Args:
            request: The request object that may contain a session cookie.
        Returns:
            The current User object, or None if not found.
        """
        session_cookies = self.session_cookie(request)
        if session_cookies is None:
            return None
        user_id = self.user_id_for_session_id(session_cookies)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session, effectively logging out the user.
        Args:
            request: The request object that may contain a session cookie.
        Returns:
            - True if the session was successfully destroyed.
            - False if the session could not be destroyed.
        """
        if request is None:
            return False
        session_cookies = self.session_cookie(request)
        if not session_cookies:
            return False
        user_id = self.user_id_for_session_id(session_cookies)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_cookies]
        return True

#!/usr/bin/env python3
"""
Session Authentication module for the API
"""
from uuid import uuid4

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """A session auth class to manage the API authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        Args:
            user_id: The ID of the user.
        Returns:
            The generated Session ID as a string,
            or None if user_id is invalid.
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        Args:
            session_id: The Session ID.
        Returns:
            The User ID associated with the Session ID,
            or None if session_id is invalid or not found.
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.
        Args:
            request: request object that may contain a session cookie.
        Returns:
            The User instance corresponding to the session cookie,
            or None if the user is not found.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout.
        Args:
            request: request object that may contain a session cookie.
        Returns:
            - True if the session was successfully destroyed.
            - False if the session could not be destroyed
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True

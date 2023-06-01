#!/usr/bin/env python3
"""
Session DBAuthentication module for the API
"""
from datetime import datetime, timedelta

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth Class"""
    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a user_id and save it to the database.
        Args:
            user_id: ID of the user for whom the session is being created.
        Returns:
            The session ID if successfully created and saved,
            or None if an error occurred.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return User ID associated with the given session ID from the database
        Args:
            session_id: session ID for which to get the corresponding User ID.
        Returns:
            The User ID if the session is valid and exists in the database,
            or None otherwise.
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        if self.session_duration <= 0:
            return user_session[0].user_id
        created_at = user_session[0].created_at
        if (created_at +
                timedelta(seconds=self.session_duration)) < datetime.utcnow():
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on the Session ID from the request\
        and remove it from the database.
        Args:
            request: The request object that may contain the session ID.
        Returns:
            - True if the session was successfully destroyed and
            removed from the database.
            - False if the session could not be destroyed
            or was not found in the database.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        user_session = UserSession.search({'session_id': session_cookie})
        if len(user_session) == 0:
            return False
        del self.user_id_by_session_id[session_cookie]
        user_session[0].remove()
        return True

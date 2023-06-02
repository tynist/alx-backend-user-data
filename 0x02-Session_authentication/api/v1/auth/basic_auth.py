#!/usr/bin/env python3
"""
Basic authentication module for the API
"""
from base64 import b64decode
from typing import Tuple, TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """A basic auth class to manage the API authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts and returns the base64 part of the Authorization header
        for Basic Auth.
        Args:
            authorization_header: The Authorization header value.
        Returns:
            The base64 part of the Authorization header,
            or None if not found.
        """
        if authorization_header is None or type(
                authorization_header
        ) is not str or authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes and returns the value of a Base64 string.
        Args:
        base64_authorization_header: base64-encoded Authorization header value
        Returns:
            The decoded value of the Base64 string, or None if decoding fails.
        """
        if base64_authorization_header is None or type(
                base64_authorization_header) is not str:
            return None
        try:
            b64_bytes = b64decode(base64_authorization_header)
            return b64_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts & return the user credentials from the decoded Base64 string
        Args:
        decoded_base64_authorization_header:decoded Authorization header value.
        Returns:
            A tuple containing the user email and password extracted from
            the decoded string, or (None, None) if the format is invalid.
        """
        if decoded_base64_authorization_header is None or type(
                decoded_base64_authorization_header
        ) is not str or ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns a User instance based on the provided email and password.
        Args:
            user_email: The email address of the user.
            user_pwd: The password of the user.
        Returns:
            The User instance if the credentials are valid,
            or None if not found or invalid.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            match = User.search({'email': user_email})
            if len(match) == 0:
                return None
            user = match[0]
            if user.is_valid_password(user_pwd):
                return user
        except Exception:
            pass
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the Authorization header.
        Args:
        request: The request object that may contain the Authorization header.
        Returns:
        The User instance if the credentials are valid and the user is found,
        or None otherwise.
        """
        header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])

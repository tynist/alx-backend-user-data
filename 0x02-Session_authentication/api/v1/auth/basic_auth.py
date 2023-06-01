#!/usr/bin/env python3
"""
Basic authentication
"""
from flask import Flask, request
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    class BasicAuth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Gets the Base64 part of the authorization header for
        the Basic Authorization
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic"):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            header_encode = base64_authorization_header.encode('utf-8')
            header_encode = b64decode(header_encode)
            header_encode = header_encode.decode('utf-8')
            return header_encode
        except BaseException:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email & password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if (":") not in decoded_base64_authorization_header:
            return None, None
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns User instance based on his email and password.
        """
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str:
            return None
        if type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except BaseException:
            return None
        if len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        header = self.extract_base64_authorization_header(header)
        header = self.decode_base64_authorization_header(header)
        user = self.extract_user_credentials(header)
        return self.user_object_from_credentials(user[0], user[1])

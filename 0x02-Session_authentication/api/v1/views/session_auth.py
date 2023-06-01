#!/usr/bin/env python3
""" Module of Session Auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from api.v1.app import auth
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Return the dictionary representation of the User
    """
    email = request.form.get('email')
    password = request.form.get('password')
    users = User.search({'email': email})
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400
    if not password or password is None:
        return jsonify({"error": "password missing"}), 400
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            session_id = auth.create_session(user.id)
            user_json = jsonify(user.to_json())
            user_json.set_cookie(os.getenv('SESSION_NAME'), session_id)
            return user_json
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout():
    """
    Destroys a session
    """
    des_session = auth.destroy_session(request)
    if des_session is False:
        abort(404)
    else:
        return jsonify({}), 200

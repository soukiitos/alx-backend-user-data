#!/usr/bin/env python3
"""Handle all routes for the Session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Define a New view for Session Authentication
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        user_found = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user_found:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_found:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    user = user_found[0]
    session_id = auth.create_session(user.id)
    SESSION_NAME = getenv("SESSION_NAME")
    res = jsonify(user.to_json())
    res.set_cookie(SESSION_NAME, session_id)
    return res


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def logout():
    """Delete the Session ID contains in the request as cookie
    """
    from api.v1.app import auth
    deleted_auth = auth.destroy_session(request)
    if not deleted_auth:
        abort(404)
    return jsonify({}), 200

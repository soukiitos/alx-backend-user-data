#!/usr/bin/env python3
"""Auth Class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Create a class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define require_auth
        """
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if path.endswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Define authorization_header
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Define current_user"""
        return None

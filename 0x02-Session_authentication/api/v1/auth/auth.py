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
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if len(path) == 0:
            return True
        exc_paths = True if path[len(path) - 1] == '/' else False
        if not exc_paths:
            path += '/'
        for excluded_path in excluded_paths:
            if len(excluded_path) == 0:
                continue
            if excluded_path[len(excluded_path) - 1] != '*':
                if path == excluded_path:
                    return False
            else:
                if excluded_path[:-1] == path[:len(excluded_path) - 1]:
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

#!/usr/bin/env python3
"""Basic auth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """BasicAuth Class
    """
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """Return the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """Return the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded_b = base64_authorization_header.encode('utf-8')
            decode_b = b64decode(encoded_b)
            decoded = decode_b.decode('utf-8')
        except BaseException:
            return None
        return decoded

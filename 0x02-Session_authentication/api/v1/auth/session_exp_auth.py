#!/usr/bin/env python3
"""Inherit from SessionAuth
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from models.user import User
from os import getenv


class SessionExpAuth(SessionAuth):
    """Create a class SessionExpAuth that inherits from SessionAuth
    """
    def __init__(self):
        """Initialize SessionExpAuth
        """
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            session_duration = int(SESSION_DURATION)
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create a Session ID by calling super()
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        dic = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        self.user_id_by_session_id[session_id] = dic
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user_id_for_session_id
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        dic = self.user_id_by_session_id.get(session_id)
        if dic is None:
            return None
        if self.session_duration <= 0:
            return dic.get('user_id')
        created_at = dic.get('created_at')
        if created_at is None:
            return None
        expired_time = created_at + timedelta(seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return dic.get('user_id')

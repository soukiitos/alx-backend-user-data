#!/usr/bin/env python3
"""
Encrypting passwords
Check valid password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Define hash_password"""
    if password:
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Define is_valid"""
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)

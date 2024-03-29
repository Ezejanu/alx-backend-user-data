#!/usr/bin/env python3

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: Salted hash of the input password.
    """

    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salted hash of the password using bcrypt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password

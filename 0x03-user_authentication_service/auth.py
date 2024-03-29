#!/usr/bin/env python3

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User
import bcrypt
import uuid


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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.

        Returns:
            User: The User object representing the newly registered user.

        Raises:
            ValueError: If a user with the given email already exists.
        """

        # Check if user with email already exists
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Create and save the user
        user = self._db.add_user(email=email, hashed_password=hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.

        Returns:
            bool: True if login is valid, False otherwise.
        """

        try:
            user = self._db.find_user_by(email=email)
            stored_password = user.hashed_password
            password_bytes = password.encode('utf-8')
            stored_password_bytes = stored_password
            return bcrypt.checkpw(password_bytes, stored_password_bytes)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user corresponding to the given email.

        Args:
            email (str): Email of the user.

        Returns:
            str: Session ID generated for the user.
        """

        try:
            # Find the user that matches with the email
            user = self._db.find_user_by(email=email)

            # Generate a new UUID for the session ID
            session_id = str(uuid.uuid4())

            # Update the user's session_id in the database
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            # Return None if no user is found for the given email
            return None


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: String representation of the new UUID.
    """
    return str(uuid.uuid4())

#!/usr/bin/env python3
"""User Model"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()


class User(Base):
    """
     SQLAlchemy model representing a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user. Non-nullable.
        hashed_password (str): The hashed password of the user. Non-nullable.
        session_id (Optional[str]): The session ID of the user, if available.
        reset_token (Optional[str]): The reset token of the user, if available.
    """

    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False)
    hashed_password: str = Column(String(length=250), nullable=False)
    session_id: Optional[str] = Column(String(length=250), nullable=True)
    reset_token: Optional[str] = Column(String(length=250), nullable=True)

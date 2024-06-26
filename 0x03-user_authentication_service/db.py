#!/usr/bin/env python3


"""DB module
"""
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The User object representing the newly added user.
        """

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The User object representing the found user.

        Raises:
            NoResultFound: If no results are found for the given query.
            exc.InvalidRequestError: If an invalid request is made.
        """

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found for the given query")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database based on user_id and keyword arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing
            user attributes to update.

        Raises:
            NoResultFound: If no user is found for the given user_id.
            ValueError: If an invalid attribute is passed in kwargs.
        """

        # Find the user by user_id
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound(f"No user found with id {user_id}") from None

        # Update user attributes
        for attr, value in kwargs.items():
            if hasattr(User, attr):
                setattr(user, attr, value)
            else:
                raise ValueError(f"Invalid attribute '{attr}'")

        # Commit changes to the database
        try:
            self._session.commit()
        except exc.InvalidRequestError as e:
            raise exc.InvalidRequestError("Invalid request") from e

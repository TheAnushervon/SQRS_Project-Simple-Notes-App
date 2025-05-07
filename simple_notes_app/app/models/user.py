"""Model for users"""
from sqlalchemy import Column, Integer, String
from app.core.database import Base


class User(Base):
    """Base model for users

    Attributes:
        __tablename__: property for mapping a class to table in db
        id: An ordinal number of the user
        username: User's name
        email: Email of user
        hashed_password: User's hashed password done on auth service
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

"""Pydantic schemas for API, user-related"""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base schema of user object

    Attributes:
        username: name of the user
        email: email of the user
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Inherited schema from base for user creation

    Attributes:
        password: user's password
    """
    password: str


class UserLogin(BaseModel):
    """Base schema for users login

    Attributes:
        username: name of the user
        password: entered password
    """
    username: str
    password: str


class UserInDB(UserBase):
    """Inherited schema from base for response

    Attributes:
        id: user's ordinal number in db
    """
    id: int

    class Config:
        """Read attributes from another class

        Args:
            orm_mode: enables ORM if set to True
        """
        orm_mode = True

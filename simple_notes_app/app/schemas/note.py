"""Pydantic schemas for API, notes related"""
from pydantic import BaseModel
from datetime import datetime


class NoteBase(BaseModel):
    """Base schema of note object

    Attributes:
        title: note's title
        content: note's body
    """
    title: str
    content: str


class NoteCreate(NoteBase):
    """Inherited schema from base for note creation"""
    pass


class NoteUpdate(NoteBase):
    """Inherited schema from base for note update"""
    pass


class NoteInDB(NoteBase):
    """Inherited schema from base in response to user

    Attributes:
        id: note ordinal number in db
        created_at: when note was created
    """
    id: int
    created_at: datetime

    class Config:
        """Read attributes from another class

        Args:
            orm_mode: enables ORM if set to True
        """
        orm_mode = True

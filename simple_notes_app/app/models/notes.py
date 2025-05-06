"""Model for notes"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Note(Base):
    """Base model for notes

    Attributes:
        __tablename__: property for mapping a class to table in db
        id: An ordinal number of the note
        title: A title of the note
        content: Body of the note
        owner_id: User who owns this note
        created_at: DateTime object indicating time of note creation
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

"""Model for translation"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Translation(Base):
    """Base model for notes translation

    Attributes:
        __tablename__: property for mapping a class to table in db
        id: An ordinal number of the translation object
        note_id: Note to which this translation belongs
        src_hash: Source hash
        src_lang: From which language need to translate
        dst_lang: To which language need to translate
        created_at: DateTime object indicating time of translation creation
    """
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    src_hash = Column(String, nullable=False, index=True)
    src_lang = Column(String(5), nullable=False, default="ru")
    dst_lang = Column(String(5), nullable=False, default="en")
    translated = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

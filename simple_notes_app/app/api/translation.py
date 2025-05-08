"""Routes for translation"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.database import get_db_session
from app.dependencies.auth import get_current_user
from app.services.translation_service import contains_russian, translate_note

router = APIRouter(prefix="/api/translate", tags=["translation"])


class TranslationRequest(BaseModel):
    """Pydantic schema for translation request

    Attributes:
        text: text which need to be translated
    """
    text: str = Field(..., min_length=1, max_length=10_000)


@router.post("/")
async def translate(
    req: TranslationRequest,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user),
):
    """Route for note translation

    Args:
        req: pydantic schema with text
        db: session of database
        current_user: authorized current user

    Returns:
        translated text in dict
    """
    translated = translate_note(db, text=req.text)
    return {"translated": translated}


@router.post("/check")
async def should_translate(
    req: TranslationRequest,
    current_user: dict = Depends(get_current_user),
):
    """Route for check whether text should be translated or not

    Args:
        req: pydantic schema with text
        current_user: authorized current user

    Returns:
        bool status of translation necessity
    """
    should = contains_russian(req.text)
    return {"should_translate": should}

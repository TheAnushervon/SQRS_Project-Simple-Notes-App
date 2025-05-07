"""Routes for interaction with notes

Uses alru_cache for cahing
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.note_service import (
    create_note,
    update_note,
    delete_note,
    get_user_notes
)
from app.schemas.note import NoteCreate, NoteUpdate, NoteInDB
from app.core.database import get_db_session
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("/", response_model=list[NoteInDB])
async def get_notes(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    """Route for obtaining notes list

    Args:
        db: session for database
        current_user: details of user interacting with API

    Returns:
        list of notes with dict objects
    """
    notes = get_user_notes(db, current_user["id"])
    return notes


@router.post("/", response_model=NoteInDB)
async def create_new_note(
    note: NoteCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    """Route for creating new note

    Args:
        note: schema containing fields required for note creation
        db: session for database
        current_user: details of user interacting with API

    Returns:
        dict containing details of created note
    """
    db_note = create_note(db, note, current_user["id"])
    return db_note


@router.put("/{note_id}", response_model=NoteInDB)
async def update_existing_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    """Route for updating existing note

    Args:
        note_id: can be found in "id" field of note object
        note: schema containing fields required for note update
        db: session for database
        current_user: details of user interacting with API

    Returns:
        dict containing details of created note

    Raises:
        HTTPException: if note with such id doesn't exists or
            doesn't belongs to current user
    """
    db_note = update_note(db, note_id, note, current_user["id"])
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.delete("/{note_id}")
async def delete_existing_note(
    note_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    """Route for creating new note

    Args:
        note_id: can be found in "id" field of note object
        db: session for database
        current_user: details of user interacting with API

    Returns:
        dict containing details of created note

    Raises:
        HTTPException: if note with such id doesn't exists or
            doesn't belongs to current user
    """
    success = delete_note(db, note_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}

"""Routes for interaction with notes"""

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
    notes = get_user_notes(db, current_user["id"])
    return notes


@router.post("/", response_model=NoteInDB)
async def create_new_note(
    note: NoteCreate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    db_note = create_note(db, note, current_user["id"])
    return db_note


@router.put("/{note_id}", response_model=NoteInDB)
async def update_existing_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
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
    success = delete_note(db, note_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}

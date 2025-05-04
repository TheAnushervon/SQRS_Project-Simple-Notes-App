from sqlalchemy.orm import Session
from app.models.notes import Note
from app.schemas.note import NoteCreate, NoteUpdate


def create_note(db: Session, note: NoteCreate, user_id: int) -> Note:
    """Create a new note with transaction management."""
    db_note = Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(
    db: Session,
    note_id: int,
    note: NoteUpdate,
    user_id: int
) -> Note:
    """Update an existing note with transaction management."""
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == user_id).first()
    if not db_note:
        return None
    for key, value in note.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int, user_id: int) -> bool:
    """Delete a note with transaction management."""
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == user_id).first()
    if not db_note:
        return False
    db.delete(db_note)
    db.commit()
    return True


def get_user_notes(db: Session, user_id: int) -> list:
    """Retrieve all notes for a user."""
    return db.query(Note).filter(Note.owner_id == user_id).all()

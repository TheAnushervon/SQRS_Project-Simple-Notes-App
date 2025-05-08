"""Authorization routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["auth"])


@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db_session)):
    """Save new user in database

    Args:
        user: schema for user
        db: session of database

    Returns:
        json object with success message

    Raises:
        HTTPException: if username or email already used for register
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session)
):
    """Authenticate user and return JWT token.

    Args:
        form_data: request form with credentials from user
        db: session for database

    Returns:
        A dict with JWT token

    Raises:
        HTTPException: if user credentials aren't correct
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

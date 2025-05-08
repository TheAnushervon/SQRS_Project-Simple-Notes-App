"""Entrypoint for an application"""
from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.notes import router as notes_router
from app.api.translation import router as translation_router
from app.core.database import init_db

app = FastAPI()


init_db()


app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(translation_router)

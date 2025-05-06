"""Entrypoint for an application"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.auth import router as auth_router
from app.api.notes import router as notes_router
from app.core.database import init_db

app = FastAPI()


init_db()


app.include_router(auth_router)
app.include_router(notes_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/templates/login.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/register", response_class=HTMLResponse)
async def register():
    with open("app/templates/register.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/notes", response_class=HTMLResponse)
async def notes():
    with open("app/templates/notes.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

from __future__ import annotations
import httpx, streamlit as st
from typing import Any
from streamlit_app import API_URL

client = httpx.Client(timeout=5.0)


def _req(method: str, path: str, *, token: str | None = None,
         **kwargs) -> httpx.Response:
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{API_URL}{path}"
    return client.request(method, url, headers=headers, **kwargs)


# ----------  Auth  ---------- #
def login(username: str, password: str) -> tuple[bool, str]:
    r = _req("post", "/login",
             data={"username": username, "password": password},
             headers={"Content-Type": "application/x-www-form-urlencoded"})
    if r.status_code == 200:
        return True, r.json()["access_token"]
    return False, r.json().get("detail", "Login failed")


def signup(username: str, email: str, password: str) -> tuple[bool, str]:
    r = _req("post", "/signup",
             json={"username": username, "email": email, "password": password})
    if r.status_code == 200:
        return True, "Account created."
    return False, r.json().get("detail", "Signup failed")


# ----------  Notes  ---------- #
def get_notes(token: str) -> list[dict[str, Any]]:
    r = _req("get", "/api/notes", token=token)
    return r.json() if r.status_code == 200 else []


def create_note(token: str, title: str, content: str) -> None:
    _req("post", "/api/notes", token=token,
         json={"title": title, "content": content})


def update_note(token: str, note_id: int, title: str, content: str) -> None:
    _req("put", f"/api/notes/{note_id}", token=token,
         json={"title": title, "content": content})


def delete_note(token: str, note_id: int) -> None:
    _req("delete", f"/api/notes/{note_id}", token=token)


# ----------  Translation  ---------- #
def should_translate(token: str, text: str) -> bool:
    r = _req("post", "/api/translate/check",
             token=token, json={"text": text})
    return r.status_code == 200 and r.json().get("should_translate", False)


def translate_text(token: str, text: str) -> str:
    r = _req("post", "/api/translate", token=token, json={"text": text})
    if r.status_code == 200:
        return r.json()["translated"]
    raise RuntimeError(r.json().get("detail", "Translation failed"))

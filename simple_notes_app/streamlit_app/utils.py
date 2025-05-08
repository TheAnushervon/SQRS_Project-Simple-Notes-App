from __future__ import annotations
import httpx
from typing import Any
from streamlit_app import API_URL

client = httpx.Client(timeout=5.0, follow_redirects=True)


def _req(
    method: str, path: str, *, token: str | None = None, **kwargs
) -> httpx.Response:
    """Makes requests with headers

    Args:
        method: which method of request (PUT, GET, etc.)
        path: endpoint path
        token: auth token

    Returns:
        Response object done by httpx

    """
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{API_URL}{path}"
    return client.request(method, url, headers=headers, **kwargs)


# ----------  Auth  ---------- #
def login(username: str, password: str) -> tuple[bool, str]:
    """Handles login for user

    Args:
        username: name of the user
        password: usesr's password

    Returns:
        tuple object with status of login (True/False) and access token
    """
    r = _req(
        "post",
        "/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if r.status_code == 200:
        return True, r.json()["access_token"]
    return False, r.json().get("detail", "Login failed")


def signup(username: str, email: str, password: str) -> tuple[bool, str]:
    """Handles registration

    Args:
        username: name of the user
        email: email of the user
        password: user's password

    Returns:
        tuple object with status of sinup (True/False) and access token
    """
    r = _req(
        "post",
        "/signup",
        json={"username": username, "email": email, "password": password},
    )
    if r.status_code == 200:
        return True, "Account created."
    return False, r.json().get("detail", "Signup failed")


# ----------  Notes  ---------- #
def get_notes(token: str) -> list[dict[str, Any]]:
    """Obtain list of notes for username

    Args:
        token: user's access token

    Returns:
        list of notes in dict or empty list
    """
    r = _req("get", "/api/notes/", token=token)
    r.raise_for_status()
    return r.json() if r.status_code == 200 else []


def create_note(token: str, title: str, content: str) -> None:
    """Creation of note

    Args:
        token: user's access token
        title: note's title
        content: note's content
    """
    r = _req(
        "post", "/api/notes/",
        token=token, json={"title": title, "content": content}
    )
    r.raise_for_status()


def update_note(token: str, note_id: int, title: str, content: str) -> None:
    """Note update

    Args:
        token: user's access token
        title: note's title
        content: note's content
    """
    r = _req(
        "put",
        f"/api/notes/{note_id}/",
        token=token,
        json={"title": title, "content": content},
    )
    r.raise_for_status()


def delete_note(token: str, note_id: int) -> None:
    """Note deletion

    Args:
        token: user's access token
        note_id: ID of the note
    """
    r = _req("delete", f"/api/notes/{note_id}/", token=token)
    r.raise_for_status()


# ----------  Translation  ---------- #
def should_translate(token: str, text: str) -> bool:
    """Check whether note should be translated or not

    Args:
        token: user's access token
        text: text to be translated

    Returns:
        True if should be, otherwise False
    """
    r = _req("post", "/api/translate/check", token=token, json={"text": text})
    r.raise_for_status()
    return r.status_code == 200 and r.json().get("should_translate", False)


def translate_text(token: str, text: str) -> str:
    """Translation of given text

    Args:
        token: user's access token
        text: text to be translated

    Returns:
        translated text
    """
    r = _req("post", "/api/translate/", token=token, json={"text": text})
    r.raise_for_status()
    if r.status_code == 200:
        return r.json()["translated"]
    raise RuntimeError(r.json().get("detail", "Translation failed"))

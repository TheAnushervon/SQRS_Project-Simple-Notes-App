import os
import re
import hashlib
import httpx


from sqlalchemy.orm import Session
from app.models.translations import Translation


RUSSIAN_RE = re.compile(r"[А-Яа-яЁё]")
X_RAPID_API_KEY = os.getenv("X_RAPID_API_KEY")
X_RAPID_API_HOST = os.getenv("X_RAPID_API_HOST")

if not X_RAPID_API_KEY:
    raise RuntimeError("X_RAPID_API_KEY not defined")

if not X_RAPID_API_HOST:
    raise RuntimeError("X_RAPID_API_HOST not defined")


def _src_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _translate_text(text: str, src_lang: str = "ru", dst_lang: str = "en") -> str:
    endpoint = "language/translate/v2"
    url = "https://%s/%s" % (X_RAPID_API_HOST, endpoint)
    resp = httpx.post(
        url=url,
        json={"source": src_lang, "target": dst_lang, "q": text},
        headers={
            "x-rapidapi-key": X_RAPID_API_KEY,
            "x-rapidapi-host": X_RAPID_API_HOST,
            "Content-Type": "application/json",
        },
        timeout=5,
    )
    resp.raise_for_status()
    translated: list[str] = resp.json()["data"]["translations"]["translatedText"]
    return "".join(translated)


def translate_note(db: Session, text: str) -> str:
    h = _src_hash(text)
    tr = db.query(Translation).filter_by(src_hash=h, dst_lang="en").first()
    if tr:
        return tr.translated

    translated = _translate_text(text)
    tr = Translation(src_hash=h, src_lang="ru", dst_lang="en", translated=translated)
    db.add(tr)
    db.commit()
    return translated


def contains_russian(text: str) -> bool:
    return bool(RUSSIAN_RE.search(text))

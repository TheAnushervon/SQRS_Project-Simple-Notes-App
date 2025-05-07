import streamlit as st
from datetime import datetime
from streamlit_app.utils import (get_notes, create_note, update_note,
                     delete_note, should_translate, translate_text)

st.set_page_config(page_title="Simple Notes – Notes")

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in from the **Home** page first.")
    st.stop()

token = st.session_state.token
st.title(f"📒 {st.session_state.username}'s notes")

# ----------  New note form ---------- #
with st.form("new_note", clear_on_submit=True):
    title   = st.text_input("Title")
    content = st.text_area("Content")
    if st.form_submit_button("Add note"):
        create_note(token, title, content)
        st.rerun()

# ----------  Existing notes ---------- #
notes = get_notes(token)
if not notes:
    st.info("No notes yet — add one above.")
else:
    for n in notes:
        with st.expander(
            f"{n['title']} "
            f"({datetime.fromisoformat(n['created_at']).strftime('%Y‑%m‑%d %H:%M')})"
        ):
            new_title   = st.text_input("Edit title", n["title"],
                                        key=f"title_{n['id']}")
            new_content = st.text_area("Edit content", n["content"],
                                        key=f"content_{n['id']}")

            cols = st.columns(3)
            with cols[0]:
                if st.button("Save", key=f"save_{n['id']}"):
                    update_note(token, n["id"], new_title, new_content)
                    st.rerun()

            with cols[1]:
                if st.button("Delete", key=f"del_{n['id']}"):
                    delete_note(token, n["id"])
                    st.rerun()

            # ----------  Translation ---------- #
            if should_translate(token, n["content"]):
                with cols[2]:
                    if st.button("Translate", key=f"tr_{n['id']}"):
                        try:
                            translated = translate_text(token, n["content"])
                            st.success("Translated text ↓")
                            st.write(translated)
                        except RuntimeError as e:
                            st.error(str(e))

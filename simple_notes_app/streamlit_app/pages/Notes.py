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
notes = sorted(get_notes(token), key=lambda n: n["created_at"], reverse=True)

for n in notes:        
    st.session_state.setdefault(f"title_state_{n['id']}", n["title"])
    st.session_state.setdefault(f"content_state_{n['id']}", n["content"])

if not notes:
    st.info("No notes yet — add one above.")
else:
    for n in notes:
        def auto_save(note_id: int):
            title_key = f"title_state_{note_id}"
            content_key = f"content_state_{note_id}"
            update_note(token, note_id,
                        st.session_state[title_key],
                        st.session_state[content_key])
            st.toast(f"Note {note_id} saved.")


        with st.expander(
            f"{n['title']} "
            f"({datetime.fromisoformat(n['created_at']).strftime('%Y-%m-%d %H:%M')})",
        ):
            st.text_input("Edit title",
                          key=f"title_state_{n['id']}",
                          on_change=auto_save,
                          args=(n['id'],))

            st.text_area("Edit content",
                         key=f"content_state_{n['id']}",
                         on_change=auto_save,
                         args=(n['id'],))
            

            cols = st.columns(2)
            with cols[0]:
                if st.button("Delete", key=f"del_{n['id']}"):
                    delete_note(token, n["id"])
                    del st.session_state[f"title_state_{n['id']}"]
                    del st.session_state[f"content_state_{n['id']}"]
                    st.rerun()

            with cols[1]:
                if should_translate(token, st.session_state[f"content_state_{n['id']}"]):
                    if st.button("Translate", key=f"tr_{n['id']}"):
                        try:
                            translated = translate_text(token, st.session_state[f"content_state_{n['id']}"])
                            st.success("Translated text ↓")
                            st.write(translated)
                        except RuntimeError as e:
                            st.error(str(e))

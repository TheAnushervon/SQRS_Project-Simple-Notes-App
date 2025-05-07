from streamlit_app.utils import login
import streamlit as st

st.set_page_config(page_title="Simple Notes – Login", page_icon="📝")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("📝 Simple Notes App")

if st.session_state.token:
    st.success(f"Logged in as **{st.session_state.username}**.")
    if st.button("Log out"):
        st.session_state.token = None
        st.rerun()
else:
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
        if submitted:
            ok, resp = login(username, password)
            if ok:
                st.session_state.token = resp
                st.session_state.username = username
                st.rerun()
            else:
                st.error(resp)

st.info("Use the sidebar to Register or manage Notes.")

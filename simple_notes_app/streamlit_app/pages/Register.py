import streamlit as st
from streamlit_app.utils import signup

st.set_page_config(page_title="Simple Notes – Register")

st.title("🆕 Register")

with st.form("register"):
    username = st.text_input("Username")
    email    = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Sign up")
    if submitted:
        ok, msg = signup(username, email, password)
        if ok:
            st.success(msg + " You can now log in from Home.")
        else:
            st.error(msg)

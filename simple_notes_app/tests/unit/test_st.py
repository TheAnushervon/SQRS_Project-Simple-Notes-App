from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import os

base_path = os.path.join("streamlit_app")


def test_register():
    with patch('streamlit_app.utils.signup',
               return_value=(True, "Registration successful")):
        at = AppTest.from_file(base_path + "/pages/Register.py").run()
        at.text_input[0].input("user1").run()
        at.text_input[1].input("some@email.ru").run()
        at.text_input[2].input("pass").run()

        at.button[0].click().run()

        assert at.success[0].value == (
            "Registration successful You can now log in from Home.")


def test_login():
    with patch('streamlit_app.utils.login',
               return_value=(True, "token")):
        at = AppTest.from_file(base_path + "/Home.py").run()

        at.text_input[0].input("user1").run()
        at.text_input[1].input("pass").run()

        at.button[0].click().run()

        assert at.session_state['token'] == "token"

        at.run()

        success_value = f"Logged in as **{at.session_state['username']}**."
        assert at.success[0].value == success_value

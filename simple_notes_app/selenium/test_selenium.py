import subprocess
import time
import uuid

from seleniumbase import BaseCase


class PageContentTest(BaseCase):

    user = f"{uuid.uuid4()}"
    password = "very_safe_password"

    @classmethod
    def setUpClass(cls) -> None:
        cls.backend_process = subprocess.Popen(
            ["uvicorn", "app.main:app", "--port", "8000"])
        cls.app_process = subprocess.Popen(
            ["streamlit", "run", "streamlit_app/Home.py"])

    def test_1_register(self) -> None:
        self.open("http://localhost:8501/Register")

        user = self.user
        email = f"{user}@example.com"
        password = self.password
        self.type("input[aria-label='Username']", user)
        self.type("input[aria-label='Email']", email)
        self.type("input[aria-label='Password']", password)
        self.click('button[data-testid="stBaseButton-secondaryFormSubmit"]')

        time.sleep(1)

        self.assert_element('div.stAlert')
        self.assert_text('Account created. You can now log in from Home.')

    def test_2_login_and_notes(self) -> None:
        self.open("http://localhost:8501")

        user = self.user
        password = self.password
        self.type("input[aria-label='Username']", user)
        self.type("input[aria-label='Password']", password)
        self.click('button[data-testid="stBaseButton-secondaryFormSubmit"]')

        time.sleep(1)

        # Notes: create
        self.assert_text(f"{user}'s notes")
        title = "new_title"
        content = "контент"
        self.type("input[aria-label='Title']", title)
        self.type("textarea[aria-label='Content']", content)
        self.click('button[data-testid="stBaseButton-secondaryFormSubmit"]')

        time.sleep(1)

        self.assert_text(f"{title}")
        self.click(f'div[data-testid="stExpander"]:contains("{title}")')

        # Notes: update
        self.assert_text("Edit title")
        title = "new_title_check"
        content = "яблоко"
        self.type("input[aria-label='Edit title']", title + "\n")
        self.click(f'div[data-testid="stExpander"]:contains("{title}")')
        self.assert_text("Edit content")
        self.type("textarea[aria-label='Edit content']", content)

        time.sleep(2)

        # Notes: translate
        self.assert_text(f"{title}")
        self.click(f'div[data-testid="stExpander"]:contains("{title}")')

        time.sleep(1)

        self.click('button:contains("Translate")')
        self.assert_text("apple")

        time.sleep(1)

        # Notes: delete
        self.click('button:contains("Delete")')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.backend_process.terminate()
        cls.backend_process.wait()
        cls.app_process.terminate()
        cls.app_process.wait()

from locust import HttpUser, task, between
import uuid


class WebsiteUser(HttpUser):
    username = None
    email = None
    token = None
    wait_time = between(1, 2)

    @task(1)
    def register(self):
        self.username = f"user_${uuid.uuid4()}"
        self.email = f"user_${uuid.uuid4()}@example.com"
        self.client.post("/signup",
                         headers={"accept": "application/json"},
                         json={
                             "username": self.username,
                             "email": self.email,
                             "password": "string"
                         },
                         name="/signup/")

    @task(1)
    def login(self):
        if self.username:
            data = {"username": self.username, "password": "string"}
            response = self.client.post("/login", data=data, name="/login/")
            self.token = "Bearer " + response.json()["access_token"]

    @task(1)
    def get_note(self):
        if self.token:
            self.client.get(
                "/api/notes/", headers={"accept": "application/json",
                                        "Authorization": self.token},
                name="/api/notes/")

    @task(3)
    def post_note(self):
        if self.token:
            request = {"title": "string",
                       "content": "string"}
            self.client.post(
                "/api/notes/",
                headers={"accept": "application/json",
                         "Authorization": self.token},
                json=request,
                name="/api/notes/")

    @task(3)
    def put_note(self):
        if self.token:
            response = self.client.get(
                "/api/notes/", headers={"accept": "application/json",
                                        "Authorization": self.token},
                name="/api/notes/")
            notes_list = response.json()

            if notes_list:
                new_request = {"title": "titlle",
                               "content": "string"}
                self.client.put(
                    f"/api/notes/{notes_list.pop()["id"]}",
                    headers={"accept": "application/json",
                             "Authorization": self.token},
                    json=new_request, name="/api/notes/{note_id}")

    @task(3)
    def delete_note(self):
        if self.token:
            response = self.client.get(
                "/api/notes/", headers={"accept": "application/json",
                                        "Authorization": self.token},
                name="/api/notes/")
            notes_list = response.json()

            if notes_list:
                self.client.delete(
                    f"/api/notes/{notes_list.pop()["id"]}",
                    headers={"accept": "application/json",
                             "Authorization": self.token},
                    name="/api/notes/{note_id}")

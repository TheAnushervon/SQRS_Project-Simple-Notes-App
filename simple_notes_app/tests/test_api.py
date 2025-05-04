from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_register():
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": "str",
                               "email": "user@example.com",
                               "password": "string"
                           })
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_login():
    data = {"username": "str", "password": "string"}
    response = client.post("/login/", data=data)
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_get_api_notes():
    data = {"username": "str", "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    response = client.get(
        "/api/notes/", headers={"accept": "application/json",
                                "Authorization": token})
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_post_api_notes():
    data = {"username": "str", "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    request = {"title": "string",
               "content": "string"}
    response = client.post(
        "/api/notes/", headers={"accept": "application/json",
                                "Authorization": token}, json=request)
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")



def test_put_api_notes():
    data = {"username": "str", "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    request = {"title": "str",
               "content": "string"}
    response = client.put(
        "/api/notes/1/", headers={"accept": "application/json",
                                  "Authorization": token}, json=request)
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")
    


def test_delete_api_notes():
    data = {"username": "str", "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    response = client.delete(
        "/api/notes/1/", headers={"accept": "application/json",
                                  "Authorization": token})
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")

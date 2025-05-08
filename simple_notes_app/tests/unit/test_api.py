"""Unit tests for app"""
import uuid
from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_register():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.json()} {username}")


def test_login():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
    response = client.post("/login/", data=data)
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_incorrect_login():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "incorrect"}
    response = client.post("/login/", data=data)
    if response.status_code != 401:
        raise AssertionError(f"Expected 401, got {response.status_code}")


def test_get_api_notes():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    response = client.get(
        "/api/notes/", headers={"accept": "application/json",
                                "Authorization": token})
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_post_api_notes():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
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
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    request = {"title": "title",
               "content": "string"}
    response = client.post(
        "/api/notes/", headers={"accept": "application/json",
                                "Authorization": token}, json=request)
    new_request = {"title": "titlle",
                   "content": "string"}
    note_id = response.json()["id"]
    response = client.put(
        f"/api/notes/{note_id}/",
        headers={"accept": "application/json",
                 "Authorization": token},
        json=new_request)
    if response.status_code != 200:
        raise AssertionError(
            f"Expected 200, got {response.status_code} {response.json()}")


def test_delete_api_notes():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    request = {"title": "title",
               "content": "string"}
    response = client.post(
        "/api/notes/", headers={"accept": "application/json",
                                "Authorization": token}, json=request)
    note_id = response.json()["id"]
    response = client.delete(
        f"/api/notes/{note_id}/", headers={"accept": "application/json",
                                           "Authorization": token})
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")


def test_translate():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    request = {"text": "яблоко"}
    response = client.post(
        "/api/translate/", headers={"accept": "application/json",
                                    "Authorization": token}, json=request)
    if response.status_code != 200:
        raise AssertionError(f"Expected 200, got {response.status_code}")

    translated = response.json()["translated"]
    if translated != "apple":
        raise AssertionError(f"Expected correct translation, got {translated}")


def test_check_translate():
    username = f"user_${uuid.uuid4()}"
    email = f"user_${uuid.uuid4()}@example.com"
    response = client.post("/signup/",
                           headers={"accept": "application/json"},
                           json={
                               "username": username,
                               "email": email,
                               "password": "string"
                           })
    data = {"username": username, "password": "string"}
    response = client.post("/login/", data=data)

    token = "Bearer " + response.json()["access_token"]
    request = {"text": "яблоко"}
    response = client.post(
        "/api/translate/check/",
        headers={"accept": "application/json",
                 "Authorization": token},
        json=request)

    check = response.json()["should_translate"]
    if check is not True:
        raise AssertionError(f"Expected True, got {check}")

    request = {"text": "apple"}
    response = client.post(
        "/api/translate/check/",
        headers={"accept": "application/json",
                 "Authorization": token},
        json=request)

    check = response.json()["should_translate"]
    if check is not False:
        raise AssertionError(f"Expected False, got {check}")

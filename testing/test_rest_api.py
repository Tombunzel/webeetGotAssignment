import pytest
import json
import requests


def login_for_token():
    """helper function fetching token for guarded endpoints"""
    login_url = "http://127.0.0.1:5000/login"

    login_data = {
        'username': 'user',
        'password': 'password'
    }
    r = requests.post(login_url, json=login_data)
    response_data = json.loads(r.text)
    token = response_data["token"]
    return token


def test_get_characters():
    """test GET all characters"""
    url = "http://127.0.0.1:5000/api/characters"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    for character in data:
        assert isinstance(character, dict)
        assert "id" in character
        assert "name" in character


def test_add_character():
    """test POST character"""
    url = "http://127.0.0.1:5000/api/characters"
    token = login_for_token()
    new_character = {"name": "Dummy Character"}
    response = requests.post(url, headers={"Authorization": token}, json=new_character)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    # Check if the character was created (specifics depend on your mock API's response)
    data = response.json()
    assert "id" in data
    assert data["name"] == "Dummy Character"


def test_update_character():
    """test PUT character"""
    character_id = 95  # adjust accordingly before running test
    url = f"http://127.0.0.1:5000/api/characters/{character_id}"
    token = login_for_token()
    updated_character = {"name": "Updated Dummy Character", "role": "Testing"}
    response = requests.put(url, headers={"Authorization": token}, json=updated_character)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Verify update was successful
    data = response.json()
    assert data["id"] == character_id
    assert data["name"] == updated_character["name"]
    assert data["role"] == updated_character["role"]


def test_delete_character():
    """test DELETE character"""
    character_id = 95  # adjust accordingly before running test
    url = f"http://127.0.0.1:5000/api/characters/{character_id}"
    token = login_for_token()
    response = requests.delete(url, headers={"Authorization": token})

    assert response.status_code == 204
    assert response.text == ""  # Verify an empty response body

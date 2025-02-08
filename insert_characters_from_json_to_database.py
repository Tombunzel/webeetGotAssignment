import requests
import json


def insert_characters_from_json_to_database():
    """helper function to transfer the characters from 'characters.json' to the database"""
    login_url = "http://127.0.0.1:5000/login"

    login_data = {
        'username': 'user',
        'password': 'password'
    }
    r = requests.post(login_url, json=login_data)
    response_data = json.loads(r.text)
    token = response_data["token"]

    add_character_url = "http://127.0.0.1:5000/api/characters"

    with open('characters.json', 'r') as filehandle:
        json_content = filehandle.read()
        characters = json.loads(json_content)
        for character in characters:
            r = requests.post(add_character_url, headers={"Authorization": token}, json=character)
            print(r.status_code)  # print status code as feedback

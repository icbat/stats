import requests
import random
import string

local_server = 'http://localhost:5000'

def random_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

def test_no_longer_supports_random_collection_names():
    """This app used to support arbitrary naming. However, with a move to redis, we now only support a handful of routes by literal name"""
    response = requests.get(f"{local_server}/{random_string()}")

    assert response.status_code == 404

def test_total_launches():
    before = requests.get(f"{local_server}/launch")

    insert = requests.post(f"{local_server}/launch")

    assert insert.status_code == 204
    assert insert.text == ""

    fetch = requests.get(f"{local_server}/launch")

    assert fetch.status_code == 200
    assert int(fetch.json()["total"]) == int(before.json()["total"]) + 1

# def test_total_game_starts():
#     before = requests.get(f"{local_server}/gameStart")

#     assert before.json()["total"] == 0

    # insert = requests.post(f"{local_server}/launch")

    # assert insert.status_code == 204
    # assert insert.text == ""

    # fetch = requests.get(f"{local_server}/launch")

    # assert fetch.status_code == 200
    # assert int(fetch.text) == int(before) + 1


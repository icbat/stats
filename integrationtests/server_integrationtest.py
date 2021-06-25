import requests
import random
import string

local_server = 'http://localhost:5000'

def random_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

def test_post_rejects_no_json():
    r = requests.post(f"{local_server}/{random_string()}")

    # why did I make it return 200 here? I hate it.
    assert r.status_code == 200
    # weird that it doesn't hit the right error message, I wonder why that is
    assert r.json()['message'] == 'malformed JSON was provided'

def test_post_rejects_bad_json():
    r = requests.post(f"{local_server}/{random_string()}", data="I'm Jason, not JSON")

    # why did I make it return 200 here? I hate it.
    assert r.status_code == 200
    assert r.json()['message'] == 'malformed JSON was provided'

def test_post_accepts_empty_bodies():
    r = requests.post(f"{local_server}/{random_string()}", json={})
    
    assert r.status_code == 200
    assert "timestamp" in r.json().keys()
    assert len(r.json().keys()) == 1

def test_get_unfilled_collection_empty_array():
    r = requests.get(f"{local_server}/{random_string()}")

    assert r.status_code == 200
    assert r.json()['data'] == []
    assert r.json()['total'] == 0

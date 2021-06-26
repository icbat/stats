import requests
import random
import string

local_server = "http://localhost:5000"


def random_string():
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


def test_no_longer_supports_random_collection_names():
    """This app used to support arbitrary naming. However, with a move to redis, we now only support a handful of routes by literal name"""
    response = requests.get(f"{local_server}/{random_string()}")

    assert response.status_code == 404


def test_total_launches():
    before_req = requests.get(f"{local_server}/launch")
    before = before_req.json()

    insert = requests.post(f"{local_server}/launch")

    assert insert.status_code == 204
    assert insert.text == ""

    fetch_req = requests.get(f"{local_server}/launch")

    assert fetch_req.status_code == 200

    fetch = fetch_req.json()
    assert int(fetch["total"]) == int(before["total"]) + 1


def test_distinct_launches():
    """each device should generate and save a UUID and send it with every request so we can tell how many unique devices are using the apps"""
    before_req = requests.get(f"{local_server}/launch/distinct")
    before = before_req.json()

    requests.post(f"{local_server}/launch", json={"uuid": "jackhayful"})
    requests.post(f"{local_server}/launch", json={"uuid": "jackhayful"})
    requests.post(f"{local_server}/launch", json={"uuid": "jackhayful"})
    requests.post(f"{local_server}/launch", json={"uuid": "hoopesorshutt"})
    new_unique_name = random_string()
    requests.post(f"{local_server}/launch", json={"uuid": new_unique_name})
    requests.post(f"{local_server}/launch", json={"uuid": new_unique_name})

    fetch_req = requests.get(f"{local_server}/launch/distinct")

    assert fetch_req.status_code == 200

    fetch = fetch_req.json()
    assert int(fetch["total"]) > int(before["total"])
    assert int(fetch["total"]) <= int(before["total"]) + 3


def test_submitting_launches_without_anything_graceful():
    """we should still collect launches even if you don't send JSON to this endpoint"""
    insert = requests.post(f"{local_server}/launch")

    assert insert.status_code == 204


def test_submitting_launches_without_json_graceful():
    """we should still collect launches even if you don't send a UUID in your JSON to this endpoint"""
    insert = requests.post(f"{local_server}/launch", data="I'm Jason, not JSON")

    assert insert.status_code == 204


def test_submitting_launches_without_uuid_graceful():
    """we should still collect launches even if you don't send a UUID in your JSON to this endpoint"""
    insert = requests.post(
        f"{local_server}/launch",
        json={"something else entirely": "definitely not what we expect"},
    )

    assert insert.status_code == 204


def test_total_game_starts():
    before_req = requests.get(f"{local_server}/gameStart")
    before = before_req.json()

    insert = requests.post(f"{local_server}/gameStart")

    assert insert.status_code == 204
    assert insert.text == ""

    fetch_req = requests.get(f"{local_server}/gameStart")

    assert fetch_req.status_code == 200

    fetch = fetch_req.json()
    assert int(fetch["total"]) == int(before["total"]) + 1


def test_daily_highscore_legacy_format():
    """vertiblocks currently uses this endpoint to determine today's highscore. this app is hard to change at the moment, so keep this format sacred"""
    fetch = requests.get(f"{local_server}/score/today")

    json = fetch.json()

    assert "data" in json.keys()
    for score in json["data"]:
        assert "score" in score.keys()


def build_score_payload(score):
    """this is what vertiblocks sends as its score payloads. currently the most complicated one"""
    formatedObstacle = {
        "name": random_string(),
        "x": random.randint(0, 100),
        "speed": random.randint(10, 50),
        "level": random.randint(1, 500),
    }

    return {
        "score": score,
        "uuid": random_string(),
        "runDuration": random.randint(1234, 999999),
        "diedTo": formatedObstacle,
    }


def test_daily_highscore_fast_with_redis():
    """goal is to only send one back so the app can calculate it fast and reduce network"""
    highscore = 200
    requests.post(f"{local_server}/score", json=build_score_payload(highscore))
    requests.post(f"{local_server}/score", json=build_score_payload(highscore - 50))
    requests.post(f"{local_server}/score", json=build_score_payload(highscore - 70))
    requests.post(f"{local_server}/score", json=build_score_payload(0 - highscore))

    fetch = requests.get(f"{local_server}/score/today")

    json = fetch.json()

    assert len(json["data"]) == 1
    assert json["data"][0]["score"] == highscore


def test_submitting_scores_not_json_fails():
    failure = requests.post(f"{local_server}/score", data="I'm Jason, not JSON")

    assert failure.status_code == 400
    assert failure.text == "This endpoint requires valid JSON"


def test_submitting_scores_no_score_attribute_fails():
    failure = requests.post(
        f"{local_server}/score", json={"name": "not really a score I guess"}
    )

    assert failure.status_code == 400
    assert failure.text == "Submitting a new score must include a score attribute"


def test_getting_alltime_high_format():
    requests.post(f"{local_server}/score", json=build_score_payload(200))

    fetch = requests.get(f"{local_server}/score/alltime")

    assert fetch.status_code == 200

    json = fetch.json()
    assert json["total"] >= 200

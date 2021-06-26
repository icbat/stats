import bottle
from redis import Redis
import argparse
from os import environ

from cors import EnableCors

if __name__ != "__main__":
    raise Exception("This file (server.py) was not meant to be imported.")

seconds_per_day = 60*60*24

app = bottle.Bottle()

print ("Reading REDIS_HOST and REDIS_PORT environment variables")
redis_host = environ["REDIS_HOST"]
redis_port = environ["REDIS_PORT"]
redis_db = environ.get("REDIS_DB", "0")
print (f"Connecting to Redis at {redis_host}:{redis_port}")
redis = Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
print (f"Pinging Redis to verify connection at {redis_host}:{redis_port}")
redis.ping()

print ("Enabling CORS for AJAX requests")
app.install(EnableCors())

def get_redis_int(key):
    result = redis.get(key) or 0
    return int(result)

### Routes
@app.get("/")
def healthCheck():
    return "I exist!"

### Posts from games
@app.post("/score")
def save_score():
    if bottle.request.json is None:
        return bottle.HTTPResponse(status=400, body="This endpoint requires valid JSON")

    input = bottle.request.json

    if "score" not in input.keys():
        return bottle.HTTPResponse(status=400, body="Submitting a new score must include a score attribute")

    score = int(input["score"])
    high_alltime = get_redis_int('top_score_alltime')
    high_today = get_redis_int('top_score_today')

    if score > high_alltime:
        redis.set('top_score_alltime', score)

    if score > high_today:
        redis.setex('top_score_today', seconds_per_day, score)

    return bottle.HTTPResponse(status=204)

@app.post("/launch")
def save_launch():
    input = bottle.request.json
    if input is not None and "uuid" in input.keys():
        redis.sadd('launched_by_uuid', input["uuid"])

    redis.incr('total_app_launches')
    return bottle.HTTPResponse(status=204)

@app.post("/gameStart")
def save_game_start():
    redis.incr('total_game_starts')
    return bottle.HTTPResponse(status=204)

### Gets from games
@app.get("/score/today")
def get_todays_scores():
    """
    used to figure out today's high score

    do not change output format, used in existing legacy apps (vertiblocks)
    """
    high_today = get_redis_int('top_score_today')

    return {"data": [ { "score": high_today } ]}

### Get for dashboards/analytics
@app.get("/launch")
def get_total_launches():
    return {"total": get_redis_int('total_app_launches')}

@app.get("/launch/distinct")
def get_total_launches():
    return {"total": redis.scard('launched_by_uuid')}

@app.get("/gameStart")
def get_total_game_starts():
    return {"total": get_redis_int('total_game_starts')}

@app.get("/score/alltime")
def get_high_score_alltime():
    return {"total": get_redis_int('top_score_alltime')}


### Actually start the app now that routes are setup
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default="5000")
parser.add_argument("--host", default="127.0.0.1")
args = parser.parse_args()

print ("Starting the server\n")
app.run(port=args.port, host=args.host)
print ("Shutting down")

### TODO figure out all the endpoints that _CAN_ change (see the gh-pages branches of the 2 apps (vert and square))

## Verti
## - get gameStart/daily_totals - this is an array of each day's daily total of game starts. maybe this is keys with the date in them that expires? how do we get those?
## - get score (then averages it out)

## TODO DAU/MAU

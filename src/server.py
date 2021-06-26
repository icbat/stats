import bottle
from redis import Redis
import argparse
from os import environ
import time
import json

from api import stats
from cors import EnableCors

if __name__ != "__main__":
    raise Exception("This file (server.py) was not meant to be imported.")

app = bottle.Bottle()

print ("Initializing")
print ("Reading ignored UUIDs from 'IGNORED_UUIDS' environment variable")
try:
    ignoredUUIDs = environ.get("IGNORED_UUIDS", "")
    ignoredUUIDs = ignoredUUIDs.split(",")
    print ("Ignoring " + str(ignoredUUIDs))
except:
    print ("Couldn't find ignored UUIDs in environment variable 'IGNORED_UUIDS'")
    ignoredUUIDs = []
logic = stats(ignoredUUIDs)

### Routes
@app.get("/")
def healthCheck():
    return "I exist!"

@app.post("/score")
def save_score():
    # TODO save the scores :)
    return bottle.HTTPResponse(status=204, body="")

@app.post("/launch")
def save_launch():
    redis.incr('total_app_launches')
    return bottle.HTTPResponse(status=204, body="")

@app.post("/gameStart")
def save_game_start():
    redis.incr('total_game_starts')
    return bottle.HTTPResponse(status=204, body="")

@app.get("/launch")
def get_total_launches():
    response = redis.get('total_app_launches') or 0
    print(response)
    print(type(response))
    return {"total": response}

@app.get("/gameStart")
def get_total_game_starts():
    response = redis.get('total_game_starts') or 0
    print(response)
    print(type(response))
    return {"total": response}

@app.get("/score/today")
def get_todays_scores():
    """
    used to figure out today's high score

    do not change output format, used in existing legacy apps
    """
    return {}

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

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default="5000")
parser.add_argument("--host", default="127.0.0.1")
args = parser.parse_args()

print ("Starting the server\n")
app.run(port=args.port, host=args.host)
print ("Shutting down")


### TODO figure out all the endpoints that cannot change

# everything here has a UUID to track who did/so we can distinct stuff out

## Square
## - post -> launch
## - post -> gameStart
## - post -> score (also includes the score)

## Verti
## - get score/today (to calculate high score, it also does a MAX on the whole collection)
## - post score (also includes score, runDuration, and diedTo)
## - post launch
## - post gameStart

### TODO figure out all the endpoints that _CAN_ change (see the gh-pages branches of the 2 apps (vert and square))

## Square
## - ????

## Verti
## - get launch
## - get launch/distinct
## - get gameStart
## - get gameStart/daily_totals
## - get score (then does some math to come up with the max)
## - get score (then averages it out)


### TODO re-architect what goes where based on all that knowledge ^^ and to work better w/ redis so we're only storing relevant data

# I'm thinking we have a set of unique UUIDs (if we even need that?)
# and things like launches/gamestarts are single metrics that are just counters

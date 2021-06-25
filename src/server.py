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

@app.get("/")
def healthCheck():
    return "I exist!"

@app.get("/<collectionName>")
def all(collectionName):
    print ("Fetching all data from collection " + collectionName)
    # rawData = list(mongodb[collectionName].find())
    rawData = list([])
    output = logic.cleanse(rawData)
    return logic.present(output)

@app.get("/<collectionName>/distinct")
def distinct(collectionName):
    print ("Fetching distinct uuids from collection " + collectionName)
    # rawData = list(mongodb[collectionName].distinct("uuid"))
    rawData = list([])
    output = [uuid for uuid in rawData if uuid not in ignoredUUIDs]
    return logic.present(output)

@app.get("/<collectionName>/daily_totals")
def daily(collectionName):
    # rawData = list(mongodb[collectionName].find())
    rawData = list([])
    rawData = logic.cleanse(rawData)
    output = logic.daily_totals(rawData)
    return output

@app.get("/<collectionName>/today")
def daily(collectionName):
    # rawData = list(mongodb[collectionName].find())
    rawData = list([])
    rawData = logic.cleanse(rawData)
    output = logic.from_today(rawData)
    return output

@app.post("/<collectionName>")
def save_new(collectionName, bottleRequest = bottle.request, systemTime = time):
    print ("Trying to save to: " + collectionName)
    try:
        for key in bottleRequest.POST.keys():
            data_point = key
        if data_point is None:
            print ("No JSON posted, will not try to save")
            return {"message": "this endpoint expects JSON"}
        data_point = json.loads(data_point)
        print ("Saving new from " + str(data_point) + " to collection '" + collectionName + "'")
    except:
        print ("Could not parse JSON provided, will not try to save")
        return {"message": "malformed JSON was provided"}

    data_point["timestamp"] = systemTime.time()
    # mongodb[collectionName].insert_one(data_point)
    print ("Save was successful!")
    return data_point


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

print ("Reading REDIS_HOST and REDIS_PORT environment variables")
redis_host = environ["REDIS_HOST"]
redis_port = environ["REDIS_PORT"]
redis_db = environ.get("REDIS_DB", "0")
print (f"Connecting to Redis at {redis_host}:{redis_port}")
redis = Redis(host=redis_host, port=redis_port, db=redis_db)

print ("Enabling CORS for AJAX requests")
app.install(EnableCors())

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default="5000")
parser.add_argument("--host", default="127.0.0.1")
args = parser.parse_args()

print ("Starting the server\n")
app.run(port=args.port, host=args.host)
print ("Shutting down")

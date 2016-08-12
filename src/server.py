import bottle
from bottle import Bottle, request, static_file, template, debug, response
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps, loads
from os import environ
import time
import json
from math import floor
from api import stats


print ("Initializing")
print ("Reading ignored UUIDs from 'IGNORED_UUIDS' environment variable")
try:
    ignoredUUIDs = environ["IGNORED_UUIDS"]
    ignoredUUIDs = ignoredUUIDs.split(",")
    print ("Ignoring " + str(ignoredUUIDs))
except:
    print ("Couldn't find ignored UUIDs in environment variable 'IGNORED_UUIDS'")
    ignoredUUIDs = []
logic = stats(ignoredUUIDs)

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
            response.headers['Access-Control-Allow-Headers'] = ''

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

app = Bottle()


@app.get("/")
def healthCheck():
    return "I exist!"

@app.get("/<collectionName>")
def all(mongodb, collectionName):
    print ("Fetching all data from collection " + collectionName)
    rawData = list(mongodb[collectionName].find())
    rawData = logic.cleanse(rawData)
    return dumps({"data": rawData, "total": len(rawData)})

@app.get("/<collectionName>/distinct")
def distinct(mongodb, collectionName):
    print ("Fetching distinct uuids from collection " + collectionName)
    rawData = list(mongodb[collectionName].distinct("uuid"))
    output = [uuid for uuid in rawData if uuid not in ignoredUUIDs]    
    return dumps({"data": output, "total":len(output)})

@app.get("/<collectionName>/byUser")
def grouped(mongodb, collectionName):
    print ("Fetching data grouped by user from collection " + collectionName)
    rawData = list(mongodb[collectionName].find())
    rawData = logic.cleanse(rawData)

    output = {}
    for document in rawData:
        uuid = document['uuid']
        if uuid not in output:
            output[uuid] = []
        del document['uuid']
        output[uuid].append(document)
    return dumps(output)


@app.get("/<collectionName>/daily")
def daily(mongodb, collectionName):
    rawData = list(mongodb[collectionName].find())
    rawData = logic.cleanse(rawData)

    output = {}
    for document in rawData:
        dayStart = floor(document['timestamp'] / 86400) * 86400
        if dayStart not in output:
            output[dayStart] = []
        output[dayStart].append(document)
    return dumps(output)


@app.post("/<collectionName>")
def save_new(mongodb, collectionName, bottleRequest = request, systemTime = time):
    print ("Request received for collection " + collectionName)
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

    print ("Timestamping to data")
    data_point["timestamp"] = systemTime.time()
    print ("Saving to mongodb")
    mongodb[collectionName].insert_one(data_point)
    print ("Save was successful!")
    return dumps(data_point)

if __name__ == "__main__":
    print ("Reading db configuration from 'MONGODB_URI' environment variable")
    mongo_uri = environ["MONGODB_URI"]
    print ("Connecting to mongo")
    plugin = MongoPlugin(uri=mongo_uri, db="mydb", json_mongo=True)
    app.install(plugin)
    print ("Enabling CORS for AJAX requests")
    app.install(EnableCors())

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default="5000")
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    print ("Starting the server\n")
    app.run(port=args.port, host=args.host)
    print ("Shutting down")

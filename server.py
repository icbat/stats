import bottle
from bottle import Bottle, request, static_file, template, debug, response
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps, loads
from os import environ
import time

print ("Initializing")

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

app = Bottle()

@app.get("/")
def healthCheck():
    return "I exist!"

@app.post("/<collectionName>")
def save_new(mongodb, collectionName, bottleRequest = request, systemTime = time):
    print ("Request received for collection " + collectionName)
    try:
        data_point = bottleRequest.json
        print ("Saving new from " + str(data_point) + " to collection '" + collectionName + "'")
    except:
        print ("Could not parse JSON provided, will not try to save")
        return {"message": "malformed JSON was provided"}
    if data_point is None:
        print ("No JSON posted, will not try to save")
        return {"message": "this endpoint expects JSON"}

    print ("Adding timestamp to data")
    data_point["timestamp"] = systemTime.time()
    print ("JSON received:")
    print (dumps(data_point))
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

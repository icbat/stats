from bottle import Bottle, request, static_file, template, debug
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps, loads
from os import environ
import time

print ("Initializing")
app = Bottle()

@app.post("/<collectionName>")
def save_new(mongodb, collectionName, bottleRequest = request, systemTime = time):
    try:
        data_point = bottleRequest.json
        print ("Saving new from " + str(data_point) + " to collection '" + collectionName + "'")
    except:
        return {"message": "malformed JSON was provided"}
    if data_point is None:
        print ("No JSON posted")
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

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default="5000")
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    print ("Starting the server\n")
    app.run(port=args.port, host=args.host)
    print ("Shutting down")

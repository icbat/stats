# stats
a simple stat server

[![Build Status](https://travis-ci.org/icbat/stats.svg?branch=master)](https://travis-ci.org/icbat/stats)

## Setup

### Environment variables

* `MONGODB_URI` is a required variable that says how to connect to the linked MongoDB instance. It looks like `mongodb://<mongo-username>:<mongo-password>@host:port` When using something like mLab MongoDB on Heroku, they should provide most of this, but you'll need to add your `mongo-username` and `mongo-password`
* `IGNORED_UUIDS` is an optional comma-separated list of uuid's to remove from all results. This is handy for excluding development results from reporting while still being able to see them in the database.

### How to turn it on locally

1. using python, `virtualenv .`
1. run script `Scripts/activate`
1. `pip install -r requirements.txt`
1. `python server.py --port <port> --host <host>`

Once the server is running, you can post arbitrary JSON at `<yourServer>/<collectionName>` and it will be saved to your linked MongoDB server under collection <collectionName>

## Contributing

All of the issues in [the repository](https://github.com/icbat/stats) should be considered "help-wanted". Please submit a pull request, or open an issue.

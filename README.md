# stats
a simple stat server

[![Build Status](https://travis-ci.org/icbat/stats.svg?branch=master)](https://travis-ci.org/icbat/stats)

## Setup

1. Enviroment variable for your mongo uri `MONGODB_URI=mongodb://<dbuser>:<dbpassword>@<urlthingy>:<port>`
1. using python, `virtualenv .`
1. run script `Scripts/activate`
1. `pip install -r requirements.txt`
1. `python server.py --port <port> --host <host>`

Once the server is running, you can post arbitrary JSON at `<yourServer>/<collectionName>` and it will be saved to your linked MongoDB server under collection <collectionName>

## Config

`IGNORED_UUIDS` is a comma-separated list of uuid's to remove from all results. This is handy for excluding development results while still being able to see them in the database.

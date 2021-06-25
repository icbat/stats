# stats
a simple stat server

## Setup

### Environment variables

* `IGNORED_UUIDS` is an optional comma-separated list of uuid's to remove from all results. This is handy for excluding development results from reporting while still being able to see them in the database.

### How to turn it on locally

1. using python, `virtualenv venv`
1. run script `venv/Scripts/activate` (or `source venv/Scripts/activate` is using something like bash)
1. `pip install -r requirements.txt`
1. `python src/server.py --port <port> --host <host>`

Once the server is running, you can post arbitrary JSON at `<yourServer>/<collectionName>` and it will be saved to your linked MongoDB server under collection <collectionName>

## Contributing

All of the issues in [the repository](https://github.com/icbat/stats) should be considered "help-wanted". Please submit a pull request, or open an issue.

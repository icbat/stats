# stats
a simple stat server for collecting scores and usage for various app

## Setup

### Environment variables

* `REDIS_HOST` the URL to the Redis instance that's backthing this
* `REDIS_PORT` the port for the Redis instance that's backing this
* `REDIS_DB` the internal DB in the Redis instance to use. Optional, defaults to `0`

### How to turn it on locally

Recommend running Redis locally w/ docker with a command like `docker run --name local-redis -p 6379:6379 -d redis`

1. using python, `virtualenv venv`
1. `source venv/Scripts/activate` or however you need to activate the virtualenv (varies by OS)
1. `pip install -r requirements_localdev.txt`
1. `REDIS_HOST=localhost REDIS_PORT=<your local redis port> python src/server.py --port <port> --host <host>`

### Running tests locally

Run `pytest integrationtests/*` to execute integration tests. Integration tests require you start up the server and connect it to a database.

## Contributing

All of the issues in [the repository](https://github.com/icbat/stats) should be considered "help-wanted". Please submit a pull request, or open an issue.

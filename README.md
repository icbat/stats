# stats
a simple stat server for collecting scores and usage for various app

## Setup

### Environment variables

* `REDISTOGO_URL` The fully qualified URL to the connected Redis instance, including port and, if necessary, basic auth

### How to turn it on locally

Recommend running Redis locally w/ docker with a command like `docker run --name local-redis -p 6379:6379 -d redis`

1. using python, `virtualenv venv`
1. `source venv/Scripts/activate` or however you need to activate the virtualenv (varies by OS)
1. `pip install -r requirements_localdev.txt`
1. `REDISTOGO_URL=redis://localhost:6379 python src/server.py`

### Running tests locally

Run `pytest integrationtests/*` to execute integration tests. Integration tests require you start up the server and connect it to a database.

## Contributing

All of the issues in [the repository](https://github.com/icbat/stats) should be considered "help-wanted". Please submit a pull request, or open an issue.

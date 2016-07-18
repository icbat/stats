# stats
a simple stat server

## Setup

1. Enviroment variable for your mongo uri `MONGODB_URI=mongodb://<dbuser>:<dbpassword>@<urlthingy>:<port>`
1. using python, `virtualenv .`
1. run script `Scripts/activate`
1. `pip install -r requirements.txt`
1. `python server.py --port <port> --host <host>`

Once the server is running, you can post arbitrary JSON at `<yourServer>/<collectionName>` and it will be saved to your linked MongoDB server under collection <collectionName>

# API to communicate with blockchain using web3.py

## Overview
This API has been built using web3, fastapi and slowapi to communicate with blockchains and fetch various types of data.

## Features
This API has the following features:
1. Runs on uvicorn ASGI server
2. Interactive GUI documentation of the API using Swagger UI and ReDoc
3. Uses slowapi to limit number of requests for a given time period
4. Has Bearer Authentication feature for users
5. Handles exceptions and returns errors promptly
6. Can customize and add more networks in app -> internal -> networks.py
   (Currently only some networks like polygon, binance smart chain work with the library)

## Prerequisites
- Python 3.x installed on your system
- JSON-RPC urls of the networks you want to use

## Installation
1. Clone or download the files from this repository.
2. Open terminal and run the following:
```pip install -r requirements.txt```
3. Modify or add networks in ``network.py`` file

## Usage
- Run the following command:
   ```python main.py```
- Uvicorn will start running on ip ``127.0.0.1`` and port ``8000``
- If you want the GUI documentation, go to ``127.0.0.1:8000/docs``
- Swagger UI and ReDoc documentation served at ``/docs`` can turned off with ``app = FastAPI(docs_url=None, redoc_url=None)``
- Authenticate yourself using Bearer Auth and send requests to the API

from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import uvicorn
from web3 import Web3

from routers import transaction, block, gas, account, encode_decode, hashing
from dependencies import get_api_key, api_key_auth
from internal.networks import networks

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from pydantic import ValidationError
from internal.models import RequestPayload

limiter = Limiter(key_func=get_api_key, default_limits=["10/minute"])

app = FastAPI(dependencies=[Depends(api_key_auth)])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(transaction.router)
app.include_router(block.router)
app.include_router(gas.router)
app.include_router(account.router)
app.include_router(encode_decode.router)
app.include_router(hashing.router)

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": "Invalid request received, check your json data."}),
    )

@app.get("/chain_id")
async def chain_id(network):
    '''Get the chain id of the network.'''

    network = networks[network.lower()]
    chain_id = network.eth.chain_id
    json_data = {"chain_id": chain_id}
    return JSONResponse(content=json_data, status_code=200)


@app.get("/is_address")
async def is_address(address):
    '''Returns True if the value is one of the recognized address formats.'''

    is_address = Web3.is_address(address)
    json_data = {"is_address": is_address}
    return JSONResponse(content=json_data, status_code=200)


@app.get("/is_checksum_address")
async def is_checksum_address(address):
    '''Returns True if the value is a valid EIP55 checksummed address.'''

    is_checksum_address = Web3.is_checksum_address(address)
    json_data = {"is_checksum_address": is_checksum_address}
    return JSONResponse(content=json_data, status_code=200)


@app.get("/to_checksum_address")
async def to_checksum_address(address):
    '''Returns the EIP55 checksummed address.'''

    to_checksum_address = Web3.to_checksum_address(address)
    json_data = {"to_checksum_address": to_checksum_address}
    return JSONResponse(content=json_data, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
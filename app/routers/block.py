from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies import get_block_identifier
from internal.networks import networks
import json
import web3
from web3 import Web3

router = APIRouter()


@router.get("/get_block")
async def get_block(network, block_identifier):
    '''Get a block by number or hash from the blockchain.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)

    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        block_info = network.eth.get_block(block_identifier)
        json_string = Web3.to_json(block_info)
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=404)


@router.get("/get_block_number")
async def get_block_number(network):
    '''Get the number of the latest block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)

    network = networks[network.lower()]
    block_number = network.eth.get_block_number()
    json_data = {"block_number": block_number}
    return JSONResponse(content=json_data, status_code=200)


@router.get("/get_block_transaction_count")
async def get_block_transaction_count(network, block_identifier):
    '''Get the number of transactions in a block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        tns_count = network.eth.get_block_transaction_count(block_identifier)
        json_data = {"block_transaction_count": tns_count}
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=400)

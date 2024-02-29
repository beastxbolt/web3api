from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies import get_block_identifier
from internal.networks import networks
import json
import web3
from web3 import Web3

router = APIRouter()


@router.get("/get_balance")
async def get_balance(network, address):
    '''Get balance of an address from the blockchain.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)

    try:
        network = networks[network.lower()]
        balance = network.eth.get_balance(address)
        json_data = {"balance": f"{Web3.from_wei(balance, 'ether'):.10f}"}
        return JSONResponse(content=json_data, status_code=200)
    except web3.exceptions.InvalidAddress:
        return JSONResponse(content={"error": "Invalid address"}, status_code=400)


@router.get("/get_proof")
async def get_proof(network, account, positions, block_identifier):
    '''Get the values from an array of storage positions for the given account at the block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        proof = network.eth.get_proof(account, positions, block_identifier)
        json_string = Web3.to_json(proof)
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except web3.exceptions.InvalidAddress:
        return JSONResponse(content={"error": "Invalid address"}, status_code=400)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=404)
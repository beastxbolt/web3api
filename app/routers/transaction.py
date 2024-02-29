from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies import get_block_identifier
from internal.networks import networks
import json
import web3
from web3 import Web3

router = APIRouter()


@router.get("/get_transaction")
async def get_transaction(network, transaction_hash):
    '''Get transaction info with transaction hash.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        transaction = network.eth.get_transaction(transaction_hash)
        json_string = Web3.to_json(transaction)
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except web3.exceptions.TransactionNotFound:
        return JSONResponse(content={"error": "Invalid hash, transaction not found"}, status_code=400)


@router.get("/get_raw_transaction")
async def get_raw_transaction(network, transaction_hash):
    '''Get the raw form of a transaction'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)

    try:
        network = networks[network.lower()]
        raw_transaction = network.eth.get_raw_transaction(transaction_hash)
        json_data = {"raw_transaction": raw_transaction.hex()}
        return JSONResponse(content=json_data, status_code=200)
    except web3.exceptions.TransactionNotFound:
        return JSONResponse(content={"error": "Invalid hash, transaction not found"}, status_code=400)


@router.get("/get_transaction_receipt")
async def get_transaction_receipt(network, transaction_hash):
    '''Get transaction receipt info with transaction hash.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        transaction = network.eth.get_transaction_receipt(transaction_hash)
        json_string = Web3.to_json(transaction)
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except web3.exceptions.TransactionNotFound:
        return JSONResponse(content={"error": "Invalid hash, transaction not found"}, status_code=400)


@router.get("/get_transaction_by_block")
async def get_transaction_by_block(network, block_identifier, transaction_index):
    '''Get a transaction info at an index from a block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        transaction = network.eth.get_transaction_by_block(
            block_identifier, int(transaction_index))
        json_string = Web3.to_json(transaction)
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=400)
    except web3.exceptions.TransactionNotFound:
        return JSONResponse(content={"error": "Transaction not found at given index"}, status_code=400)


@router.get("/get_raw_transaction_by_block")
async def get_raw_transaction_by_block(network, block_identifier, transaction_index):
    '''Get the raw form of a transaction at an index from a block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        raw_transaction = network.eth.get_raw_transaction_block(
            block_identifier, transaction_index)
        json_data = {"raw_transaction": raw_transaction.hex()}
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=400)
    except web3.exceptions.TransactionNotFound:
        return JSONResponse(content={"error": "Transaction not found at given index"}, status_code=400)


@router.get("/get_uncle_by_block")
async def get_uncle_by_block(network, block_identifier, uncle_index):
    '''Get uncle at an index from a block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        uncle = network.eth.get_uncle_by_block(
            block_identifier, int(uncle_index))
        json_string = Web3.to_json(uncle)
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=400)


@router.get("/get_uncle_count")
async def get_uncle_count(network, block_identifier):
    '''Get the number of uncles in a block.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        uncle_count = network.eth.get_uncle_count(block_identifier)
        json_data = {"uncle_count": uncle_count}
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=400)


@router.get("/get_transaction_count")
async def get_transaction_count(network, account, block_identifier):
    '''Get the number of transactions sent from an address.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        block_identifier = await get_block_identifier(block_identifier)
        transaction_count = network.eth.get_transaction_count(
            account, block_identifier)
        json_data = {"transaction_count": transaction_count}
        return JSONResponse(content=json_data, status_code=200)
    except web3.exceptions.InvalidAddress:
        return JSONResponse(content={"error": "Invalid address"}, status_code=400)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=400)
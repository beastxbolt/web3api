from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies import get_block_identifier
from internal.networks import networks
import json
import web3
from web3 import Web3, middleware

router = APIRouter()


@router.get("/gas_price")
async def gas_price(network):
    '''Get standard gas price in Gwei. (Supports only legacy networks)'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)

    network = networks[network.lower()]
    gas_price = network.eth.gas_price
    json_data = {"gas_price": f"{Web3.from_wei(gas_price, 'gwei'):.10f}"}
    return JSONResponse(content=json_data, status_code=200)


@router.get("/max_priority_fee")
async def max_priority_fee(network):
    '''Get suggested max priority fee for dynamic fee transactions in Gwei'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    network = networks[network.lower()]
    fee = network.eth.max_priority_fee
    json_data = {"max_priority_fee": f"{Web3.from_wei(fee, 'gwei'):.10f}"}
    return JSONResponse(content=json_data, status_code=200)


@router.get("/fee_history")
async def fee_history(network, block_count, newest_block):
    '''Get transaction fee data in Gwei for up to 1,024 blocks.'''

    if network.lower() not in networks:
        return JSONResponse(content={"error": "Invalid network or not supported"}, status_code=400)
    
    try:
        network = networks[network.lower()]
        newest_block = await get_block_identifier(newest_block)
        fee_history = network.eth.fee_history(block_count, newest_block)
        json_string = Web3.to_json(fee_history)
        json_data = json.loads(json_string)
        base_fee_per_gas = []
        try:
            for i in json_data["baseFeePerGas"]:
                base_fee_per_gas.append(f"{Web3.from_wei(i, 'gwei'):.10f}")
            json_data["baseFeePerGas"] = base_fee_per_gas
        except:
            pass
        return JSONResponse(content=json_data, status_code=200)
    except (ValueError, web3.exceptions.BlockNotFound):
        return JSONResponse(content={"error": "Block not found"}, status_code=404)
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from web3 import Web3

router = APIRouter()


@router.get("/keccak")
async def keccak(type, value):
    '''Returns the Keccak-256 of the given value. Text is encoded to UTF-8 before computing the hash, just like Solidity.'''
    try:
        if type.lower() == "primitive":
            try:
                if value.lower() == "true":
                    value = True
                if value.lower() == "false":
                    value = False
                hex_value = Web3.keccak(primitive=value)
            except:
                try:
                    hex_value = Web3.keccak(primitive=int(value))
                except:
                    hex_value = Web3.keccak(primitive=f"{value}".encode("utf-8"))

        elif type.lower() == "hexstr":
            hex_value = Web3.keccak(hexstr=str(value))
        elif type.lower() == "text":
            hex_value = Web3.keccak(text=str(value))
        else:
            return JSONResponse(content={"error": "Invalid type"}, status_code=400)
        json_data = {"keccak_value": hex_value.hex()}
        return JSONResponse(content=json_data, status_code=200)
    except ValueError:
        return JSONResponse(content={"error": "Invalid value"}, status_code=400)
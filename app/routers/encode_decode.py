from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json
from web3 import Web3

router = APIRouter()


@router.get("/to_hex")
async def to_hex(type, value):
    '''Converts a value to its hex representation.'''
    try:
        if type.lower() == "primitive":
            try:
                if value.lower() == "true":
                    value = True
                if value.lower() == "false":
                    value = False
                hex_value = Web3.to_hex(primitive=value)
            except:
                try:
                    hex_value = Web3.to_hex(primitive=int(value))
                except:
                    hex_value = Web3.to_hex(primitive=f"{value}".encode("utf-8"))

        elif type.lower() == "hexstr":
            hex_value = Web3.to_hex(hexstr=str(value))
        elif type.lower() == "text":
            hex_value = Web3.to_hex(text=str(value))
        else:
            return JSONResponse(content={"error": "Invalid type"}, status_code=400)
        json_data = {"hex_value": hex_value}
        return JSONResponse(content=json_data, status_code=200)
    except ValueError:
        return JSONResponse(content={"error": "Invalid value"}, status_code=400)


@router.get("/to_text")
async def to_text(type, value):
    '''Converts a value to its text representation.'''
    try:
        if type.lower() == "primitive":
            try:
                if value.lower() == "true":
                    value = True
                if value.lower() == "false":
                    value = False
                hex_value = Web3.to_text(primitive=value)
            except:
                try:
                    hex_value = Web3.to_text(primitive=int(value))
                except:
                    hex_value = Web3.to_text(primitive=f"{value}".encode("utf-8"))

        elif type.lower() == "hexstr":
            hex_value = Web3.to_text(hexstr=str(value))
        elif type.lower() == "text":
            hex_value = Web3.to_text(text=str(value))
        else:
            return JSONResponse(content={"error": "Invalid type"}, status_code=400)
        json_data = {"text_value": hex_value}
        return JSONResponse(content=json_data, status_code=200)
    except ValueError:
        return JSONResponse(content={"error": "Invalid value"}, status_code=400)


@router.get("/to_bytes")
async def to_bytes(type, value):
    '''Converts a value to its bytes representation.'''
    try:
        if type.lower() == "primitive":
            try:
                if value.lower() == "true":
                    value = True
                if value.lower() == "false":
                    value = False
                hex_value = Web3.to_bytes(primitive=value)
            except:
                try:
                    hex_value = Web3.to_bytes(primitive=int(value))
                except:
                    hex_value = Web3.to_bytes(primitive=f"{value}".encode("utf-8"))

        elif type.lower() == "hexstr":
            hex_value = Web3.to_bytes(hexstr=str(value))
        elif type.lower() == "text":
            hex_value = Web3.to_bytes(text=str(value))
        else:
            return JSONResponse(content={"error": "Invalid type"}, status_code=400)
        json_data = {"bytes_value": str(hex_value)}
        return JSONResponse(content=json_data, status_code=200)
    except ValueError:
        return JSONResponse(content={"error": "Invalid value"}, status_code=400)


@router.get("/to_int")
async def to_int(type, value):
    '''Converts a value to its integer representation.'''
    try:
        if type.lower() == "primitive":
            try:
                if value.lower() == "true":
                    value = True
                if value.lower() == "false":
                    value = False
                hex_value = Web3.to_int(primitive=value)
            except:
                try:
                    hex_value = Web3.to_int(primitive=int(value))
                except:
                    hex_value = Web3.to_int(primitive=f"{value}".encode("utf-8"))

        elif type.lower() == "hexstr":
            hex_value = Web3.to_int(hexstr=str(value))
        elif type.lower() == "text":
            hex_value = Web3.to_int(text=str(value))
        else:
            return JSONResponse(content={"error": "Invalid type"}, status_code=400)
        json_data = {"int_value": hex_value}
        return JSONResponse(content=json_data, status_code=200)
    except ValueError:
        return JSONResponse(content={"error": "Invalid value"}, status_code=400)


@router.get("/to_json")
async def to_json(object):
    '''Converts a an object to its JSON representation.'''
    try:
        json_string = json.loads(Web3.to_json(object))
        json_data = json.loads(json_string)
        return JSONResponse(content=json_data, status_code=200)
    except ValueError:
        return JSONResponse(content={"error": "Invalid object"}, status_code=400)
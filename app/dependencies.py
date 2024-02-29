from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

api_keys = ["abc123", "xyz321"]
oauth2_scheme = HTTPBearer(scheme_name="Bearer", description="API Key")


def get_api_key(request: Request):
    api_key = request.headers.get("Authorization")
    return api_key


async def get_block_identifier(block_identifier):
    try:
        return int(block_identifier)
    except ValueError:
        return block_identifier


def api_key_auth(api_key: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    api_key = api_key.credentials
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

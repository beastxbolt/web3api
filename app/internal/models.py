from pydantic import BaseModel
from typing import Optional

class RequestPayload(BaseModel):
    pass

    class Config:
        extra = "allow"
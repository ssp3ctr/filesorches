from pydantic import BaseModel
from typing import Dict, Literal, Any


class StorageAdapterConfig(BaseModel):
    type: Literal["s3", "gwm", "tcp"]
    config: Dict[str, Any]
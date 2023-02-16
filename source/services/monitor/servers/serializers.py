from pydantic import BaseModel
from typing import Optional


class ServerCreateReq(BaseModel):
    server: str
    status: str
    cpu: int
    memory: int
    gpu: int = 0
    type: str = "cpu"


class NodePodCreatedBy(BaseModel):
    id: Optional[int] = 1
    username: str


class NodeDetailRes(BaseModel):
    id: int
    status: str
    server: str
    occupied_rate: str
    source: str
    occupied_by: list[NodePodCreatedBy]

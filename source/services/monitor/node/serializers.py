from pydantic import BaseModel
from typing import Optional


class NodeCreate(BaseModel):
    server: Optional[str] = "default"
    status: Optional[str] = "False"
    cpu: Optional[int] = 0
    memory: Optional[int] = 0
    gpu: Optional[int] = 0
    type: Optional[str] = "cpu"


class NodePodCreatedBy(BaseModel):
    id: int
    username: str


class NodeDetailRes(BaseModel):
    id: int
    status: str
    server: str
    occupied_rate: str
    source: str
    occupied_by: list[NodePodCreatedBy]

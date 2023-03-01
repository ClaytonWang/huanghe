from pydantic import BaseModel
from typing import Optional, List


class TaskDetail(BaseModel):
    name: str
    source: str


class PodCreatedBy(BaseModel):
    id: int
    username: str
    tasks: List[TaskDetail]


class ServerCreateReq(BaseModel):
    server_ip:str
    server: str
    status: str
    cpu: int
    memory: int
    gpu: int = 0
    type: str = "cpu"
    occupied_cpu: Optional[int] = 0
    occupied_gpu: Optional[int] = 0
    occupied_memory: Optional[int] = 0
    occupied_by: Optional[List[PodCreatedBy]] = []


class NodeDetailRes(BaseModel):
    id: int
    status: str
    server: str
    occupied_rate: str
    source: str
    occupied_by: Optional[List[PodCreatedBy]] = []
    # occupied_by: list
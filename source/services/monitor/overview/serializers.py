from pydantic import BaseModel
from typing import Optional, List


class Project(BaseModel):
    id: int
    name: Optional[str]


class ProjectReq(BaseModel):
    project: List[int]


class TaskItem(BaseModel):
    name: str
    total: int
    running: int


# class StatisticNoteBookReq(BaseModel):
#     name: str = "Notebook"
#     total: Optional[int] = 0
#     running: Optional[int] = 0
#
#
# class StatisticJobReq(BaseModel):
#     name: str = "Job"
#     total: Optional[int] = 0
#     running: Optional[int] = 0
#
#
# class StatisticRes(BaseModel):
#     result: list[StatisticNoteBookReq, StatisticJobReq]
#
#
# class OverviewCpu(BaseModel):
#     name: str="CPU"
#     occupied: int
#     used: int
#     occupied_rate: float
#
# class OverviewGpu(BaseModel):
#     name: str="GPU"
#     occupied: int
#     used: int
#     occupied_rate: float
#
# class OverviewMemory(BaseModel):
#         name: str = "内存"
#         occupied: int
#         used: int
#         occupied_rate: float
#
# class OverviewStorage(BaseModel):
#     name: str = "存储"
#     occupied: int
#     used: int
#     occupied_rate: float
# class OverviewSource(BaseModel):
#     result:[OverviewCpu,OverviewGpu,OverviewMemory,OverviewStorage]

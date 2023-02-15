from pydantic import BaseModel
from typing import Optional


class Project(BaseModel):
    id: int
    name: Optional[str]


class ProjectReq(BaseModel):
    project: list[Project]


class StatisticNoteBookReq(BaseModel):
    name: str = "Notebook"
    total: Optional[int] = 0
    running: Optional[int] = 0


class StatisticJobReq(BaseModel):
    name: str = "Job"
    total: Optional[int] = 0
    running: Optional[int] = 0


class StatisticRes(BaseModel):
    result: list[StatisticNoteBookReq, StatisticJobReq]

import re
from datetime import datetime
from fastapi import HTTPException, status
from typing import Optional, List, Union, Dict

from pydantic import BaseModel
from pydantic import validator

class TimeReq(BaseModel):
    start: str
    end: str


class SingleChart(BaseModel):
    name: str
    data:list
    unit: Optional[str]


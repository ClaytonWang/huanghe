# -*- coding: utf-8 -*-
from typing import Dict

from pydantic import BaseModel


class Event(BaseModel):
    namespace: str
    label_selector: Dict[str, str]

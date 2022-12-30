# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Dict, Optional

class Namespace(BaseModel):
    name: str

    labels: Optional[Dict] = {"istio-injection": "enabled"}
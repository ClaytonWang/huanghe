# -*- coding: utf-8 -*-
from typing import Dict

from basic.common.validator_name import Cluster


class Event(Cluster):
    namespace: str
    label_selector: Dict[str, str] = {}

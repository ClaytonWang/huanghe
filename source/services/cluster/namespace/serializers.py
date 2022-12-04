# -*- coding: utf-8 -*-

from pydantic import BaseModel


class Namespace(BaseModel):
    name: str


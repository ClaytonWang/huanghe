# -*- coding: utf-8 -*-
"""
    >File   : api.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2023/3/16 11:16
"""
import json
from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path, Query
from fastapi.responses import JSONResponse
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.common.event_model import Event
from basic.common.env_variable import get_string_variable
from basic.middleware.account_getter import AccountGetter, ProjectGetter, get_project
from basic.middleware.service_requests import get_user_list, volume_check
from utils.user_request import project_check, project_check_obj
from utils.auth import operate_auth
from collections import defaultdict
import datetime

router_deployment = APIRouter()
COMMON = "https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?"
ACCOUNT = "jovyan"
PASSWORD = "jovyan"




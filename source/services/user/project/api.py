# -*- coding: utf-8 -*-
"""
    >File    : api.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/28 19:52
"""
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from asyncpg.exceptions import UniqueViolationError
from models.project import Project
from project.serializers import ProjectCreate, ProjectList
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters



router_project = APIRouter()


@router_project.post(
    '',
    description='创建项目',
    response_model=ProjectList,
)
async def create_user(project: ProjectCreate):
    return await Project.objects.create(**project.dict())

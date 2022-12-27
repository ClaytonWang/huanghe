from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from notebook.serializers import NoteBookCreateReq, NoteBookDeleteReq, NoteBookListReq, NoteBook
from k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response


router_notebook = APIRouter()


@router_notebook.post(
    '',
    description='创建notebook',
)
def create_notebook(nbcr: NoteBookCreateReq):
    cc.create_notebook(NoteBook.parse_obj(nbcr.gen_notebook_dict()))
    return success_common_response()


@router_notebook.post(
    '/batch',
    description='批量查询notebook',
    response_model=NoteBookCreateReq,
)
def list_notebook(nblr: NoteBookListReq):
    res = cc.list_notebook(nblr)
    print(res)
    return nblr

@router_notebook.delete(
    '',
    description='删除notebook',
)
def delete_notebook(nb: NoteBookDeleteReq):
    cc.delete_notebook(nb)
    return success_common_response()
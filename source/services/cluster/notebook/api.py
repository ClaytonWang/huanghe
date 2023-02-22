from fastapi import APIRouter
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
)
def list_notebook(nblr: NoteBookListReq):
    return cc.list_notebook(nblr)


@router_notebook.delete(
    '',
    description='删除notebook',
)
def delete_notebook(nb: NoteBookDeleteReq):
    cc.delete_notebook(nb)
    return success_common_response()

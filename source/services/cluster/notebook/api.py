from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from notebook.serializers import NoteBook
from k8s.cluster_client import cc


router_notebook = APIRouter()


@router_notebook.post(
    '',
    description='创建notebook',
    response_model=NoteBook,
)
def create_namespace(nb: NoteBook):
    cc.create_notebook(nb)
    return nb
#
# @router_pvc.delete(
#     '',
#     description='删除存储卷',
#     response_model=PVC,
# )
# def delete_namespace(pvc: PVC):
#     cc.delete_namespace(pvc)
#     return pvc
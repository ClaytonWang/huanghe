from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from notebook.serializers import NoteBookCreateReq, NoteBookDeleteReq, NoteBook
from k8s.cluster_client import cc


router_notebook = APIRouter()


@router_notebook.post(
    '',
    description='创建notebook',
    response_model=NoteBookCreateReq,
)
def create_notebook(nbcr: NoteBookCreateReq):
    cc.create_notebook(NoteBook.parse_obj(nbcr.gen_notebook_dict()))
    return nbcr

@router_notebook.delete(
    '',
    description='删除notebook',
    response_model=NoteBook,
)
def delete_notebook(nb: NoteBookDeleteReq):
    cc.delete_notebook(nb)
    return nb
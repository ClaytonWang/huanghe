from fastapi import APIRouter
from volcanojob.serializers import VolcanoJobCreateReq, VolcanoJobDeleteReq, VolcanoJob
from k8s.cluster_client import cc
from basic.middleware.rsp import success_common_response


router_vcjob = APIRouter()


@router_vcjob.post(
    '',
    description='创建vcjob',
)
def create_vcjob(vjcr: VolcanoJobCreateReq):
    cc.create_vcjob(VolcanoJob.parse_obj(vjcr.gen_vcjob_dict()))
    return success_common_response()

#
# @router_notebook.post(
#     '/batch',
#     description='批量查询notebook',
# )
# def list_notebook(nblr: NoteBookListReq):
#     return cc.list_notebook(nblr)
#
# @router_notebook.delete(
#     '',
#     description='删除notebook',
# )
# def delete_notebook(nb: NoteBookDeleteReq):
#     cc.delete_notebook(nb)
#     return success_common_response()
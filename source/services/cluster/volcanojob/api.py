from fastapi import APIRouter
from volcanojob.serializers import VolcanoJobCreateReq, VolcanoJobDeleteReq, VolcanoJob, VolcanoStatusPostReq
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


@router_vcjob.post(
    '/status/test',
    description='创建vcjob',
)
def update_status(vspr: VolcanoStatusPostReq):
    print(vspr.name)
    print(vspr.status)
    return success_common_response()


#
# @router_notebook.post(
#     '/batch',
#     description='批量查询notebook',
# )
# def list_notebook(nblr: NoteBookListReq):
#     return cc.list_notebook(nblr)
#
@router_vcjob.delete(
    '',
    description='删除vcjob',
)
def delete_vcjob(vjdr: VolcanoJobDeleteReq):
    cc.delete_vcjob(vjdr)
    return success_common_response()

from fastapi import APIRouter
from volcanojob.serializers import VolcanoJobCreateReq,VolcanoJobListReq, VolcanoJobDeleteReq, VolcanoJob
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
    '/batch',
    description='批量查询vcjob',
)
def list_volcanojob(vjlr: VolcanoJobListReq):
    res=cc.list_volcanojob(vjlr)
    return res

@router_vcjob.delete(
    '',
    description='删除volcanojob'
)
def delete_volcanojob(vjdr: VolcanoJobDeleteReq):
    cc.delete_vcjob(vjdr)
    return success_common_response()
from fastapi import APIRouter, Depends, Request, HTTPException, status, Path, Query

from basic.middleware.account_getter import AccountGetter
from basic.utils.async_task import AsyncTask
from services.job_management.job.serializers import JobOpReq, JobEditReq, JobCreate
from services.job_management.models.job import Job
from services.job_management.utils.auth import operate_auth
from services.job_management.utils.user_request import project_check_obj


async def verify_auth(request: Request, job_id: int = Path(..., ge=1, description="JobID")):
    _job, reason = await operate_auth(request, job_id)
    if not _job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)
    return _job


async def verify_project_check(request: Request, je: JobEditReq,
                               job_id: int = Path(..., ge=1, description="JobID"), _job: Job = Depends(verify_auth)):
    ag: AccountGetter = request.user
    async_task = AsyncTask()
    async_task.add_task(project_check_obj(request, je.project.id))
    async_task.add_task(Job.objects.filter(name=_job.name, project_by_id=int(je.project.id),
                                           created_by_id=ag.id).exclude(id=job_id).count())
    (check, extra_info), count = await async_task.run_tasks()
    if not check:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=extra_info['en_name'])

    if count:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户，Job不能重名')

    return extra_info


async def verify_create_same_job(request: Request, jc: JobCreate):
    ag: AccountGetter = request.user
    if await Job.objects.filter(name=jc.name, project_by_id=jc.project.id, created_by_id=ag.id).count():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='同一个项目下，同一个用户, job不能重名')


async def verify_status_name(_job: Job = Depends(verify_auth)):
    if _job.status.name not in {'stopped', "completed", "run_fail"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job未停止')


async def verify_job_related_status(job_id: int = Path(..., ge=1, description="JobID")):
    job = await Job.get_job_related_status_by_pk(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job不存在")
    return job

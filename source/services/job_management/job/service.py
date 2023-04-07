import datetime
import json

from fastapi import HTTPException
from starlette import status

from basic.common.base_config import ADMIN, ENV
from basic.common.event_model import Event
from basic.common.paginate import *
from basic.common.query_filter_params import QueryParameters
from basic.middleware.account_getter import AccountGetter, ProjectGetter, VolcanoJobCreateReq, delete_vcjob, \
    create_vcjob, VolcanoJobDeleteReq
from basic.middleware.service_requests import volume_check
from basic.utils.source import source_convert
from services.job_management.job.serializers import JobEditReq, JobOpReq, EventItem, EventCreate
from services.job_management.models.job import Job
from services.job_management.models.mode import Mode
from basic.common.status_cache import sc


async def list_mode():
    return await Mode.mode_cache_pagation()


async def count_job_by_project_id(project_id: int, user_id: int):
    if user_id:
        job_count = await Job.self_project_and_self_view(project_id=project_id, self_id=user_id)
    else:
        job_count = await Job.self_project(project_id)
    return job_count


async def list_project_by_ip(server_ip: str):
    return await Job.project_list_by_ip(server_ip)


async def list_job_by_role(name, id):
    if name == ADMIN:
        jobs = await Job.all_jobs()
    else:
        jobs = await Job.self_view(id)
    return jobs


async def list_simple_job(params_filter, user: AccountGetter):
    jobs = await list_job_by_role(user.role.name, user.id)

    query = await jobs.select_related('status').filter(**params_filter).all()

    res = [x.gen_job_simple_response() for x in query]
    return res


async def get_detail_job_by_id(job_id):
    _job = await Job.objects.select_related(
        ['status', "start_mode"]
    ).get(pk=job_id)
    return _job.gen_job_detail_response()


async def list_job(user: AccountGetter, query_params):
    jobs = await list_job_by_role(user.role.name, user.id)
    p = await paginate(jobs.select_related(
        'status'
    ).order_by(Job.updated_at.desc()).filter(
        **query_params.filter_
    ), params=query_params.params)

    return p


async def save_job(jc, authorization: str, ag: AccountGetter, pg: ProjectGetter):
    # 存储检查
    storages, volumes_k8s = await volume_check(authorization, jc.hooks, pg.en_name)

    machine_type, gpu_count, cpu_count, memory = source_convert(jc.source)
    start_mode = await Mode.get(jc.start_mode.id)

    k8s_info = VolcanoJobCreateReq(name=f"{ag.en_name}-{jc.name}",
                                   namespace=pg.en_name,
                                   image=jc.image.name,
                                   env=ENV,
                                   cpu=cpu_count,
                                   memory=memory,
                                   gpu=gpu_count,
                                   volumes=volumes_k8s,
                                   command=[jc.start_command],
                                   working_dir=jc.work_dir,
                                   task_num=jc.nodes,
                                   mode=start_mode, ).dict()

    init_data = {"name": jc.name,
                 "created_by_id": ag.id,
                 "updated_by_id": ag.id,
                 "create_en_by": ag.en_name,
                 "created_by": ag.username,
                 "updated_by": ag.username,
                 "status": sc.get('stopped'),
                 "project_by_id": pg.id,
                 "project_by": pg.name,
                 "project_en_by": pg.en_name,
                 "mode": jc.mode,
                 "start_command": jc.start_command,
                 "custom": jc.image.custom,
                 "image": jc.image.name,
                 "work_dir": jc.work_dir,
                 "k8s_info": json.dumps(k8s_info),
                 "storage": json.dumps(storages),
                 "cpu": cpu_count,
                 "gpu": gpu_count,
                 "memory": memory,
                 "type": machine_type,
                 "start_mode": jc.start_mode.id,
                 "nodes": jc.nodes,
                 }

    _job = await Job.objects.create(**init_data)
    k8s_info['annotations'] = {"id": str(_job.id), "gpu": str(gpu_count), "slots": str(gpu_count) if gpu_count else "1"}
    await _job.update(**{"k8s_info": k8s_info})
    return _job


async def update_status(jsu_status: str, jsu_server_ip: str, job: Job):
    st = Job.compare_status_and_update(jsu_status, sc)
    update_data = {"status": st}
    if jsu_status in {"Failed", "Completed", "Terminated"}:
        update_data.update({"ended_at": datetime.datetime.now()})
    if jsu_server_ip:
        update_data['server_ip'] = jsu_server_ip
    await job.update(**update_data)
    return job


async def update_job(authorization: str, je: JobEditReq, _job: Job, k8s_info: dict, extra_info: dict, username: str):
    update_data = {}
    start_mode = await Mode.get(je.start_mode.id)

    if je.source:
        machine_type, gpu_count, cpu_count, memory = source_convert(je.source)
        source_dic = {'cpu': cpu_count,
                      'memory': memory,
                      'gpu': gpu_count,
                      'type': machine_type,
                      }
        k8s_info.update(source_dic)
        k8s_info['annotations'] = {"id": str(_job.id), "gpu": str(gpu_count),
                                   "slots": str(gpu_count) if gpu_count else "1"}
        update_data = source_dic

    storages, volumes_k8s = await volume_check(authorization, je.hooks, extra_info['en_name'])
    k8s_info.update({"volumes": volumes_k8s,
                     'image': je.image.name,
                     'namespace': extra_info['en_name'],
                     'name': f"{username}-{_job.name}",
                     "command": [je.start_command],
                     "work_dir": je.work_dir,
                     "task_num": je.nodes,
                     "mode": start_mode,
                     })
    update_data.update({"storage": json.dumps(storages),
                        "k8s_info": json.dumps(k8s_info),
                        "updated_at": datetime.datetime.now(),
                        "project_by_id": je.project.id,
                        "project_by": extra_info['name'],
                        "image": je.image.name,
                        "custom": je.image.custom,
                        "work_dir": je.work_dir,
                        'status': sc.get('stopped'),
                        "mode": je.mode,
                        "start_command": je.start_command,
                        "start_mode": je.start_mode.id,
                        "nodes": je.nodes,
                        })
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')
    return _job


async def update_job_by_operate(job_op: JobOpReq, payloads: str, _job: Job):
    update_data = {}
    if job_op.action == 0:
        update_data['status'] = sc.get('stopped')
        delete_vcjob(vjd=VolcanoJobDeleteReq.parse_raw(payloads), ignore_no_found=True)
        await _job.update(**{"ended_at": datetime.datetime.now()})
    elif job_op.action == 1:
        update_data['status'] = sc.get('pending')
        create_vcjob(vjc=VolcanoJobCreateReq.parse_raw(payloads))
        await _job.update(**{"started_at": datetime.datetime.now()})

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新数据不能为空')
    if not await _job.update(**update_data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Job不存在')

    return _job


async def delete_job(_job: Job):
    payloads = _job.k8s_info
    # error状态调用删除需要释放资源
    if _job.status.name != 'stop':
        delete_vcjob(vjd=VolcanoJobDeleteReq.parse_obj(dict(payloads)), ignore_no_found=True)
    await _job.delete()


async def list_job_event(job_id: int, query_params: QueryParameters):
    params_filter = query_params.filter_
    events = await Event.find_vcjob_events(job_id)
    events = await paginate(events.filter(**params_filter), params=query_params.params)
    for i, v in enumerate(events.data):
        events.data[i] = EventItem.parse_obj(v.gen_pagation_event())
    return events


async def save_job_event(ec: EventCreate, job_id: int):
    j = await Job.objects.select_related(['status']).get(pk=job_id)
    d = ec.dict()
    d.update({"status": j.status.desc})
    await Event.objects.create(**d)

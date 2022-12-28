# -*- coding: utf-8 -*-
"""
    >File   : scheduler_task.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/22 18:55
"""


import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.base import BaseJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from utils.user_request import get_current_user_aio
from utils.k8s_request import list_notebook_k8s
from models.notebook import Notebook, Status
from utils.k8s_request import list_notebook_k8s, NoteBookListReq
from models.initdb import startup_event

async def job_func(job_id):
    await startup_event()
    print(f"job {job_id} run in {datetime.now()}")
    notebooks = list_notebook_k8s(NoteBookListReq())
    notebook_dic = {}
    for notebook in notebooks:
        name = notebook['name']
        namespace = notebook['namespace']
        status = notebook['status']
        url = notebook['url']
        notebook_dic[f'{name}-{namespace}'] = {"status": status, 'url': url}
    print(notebook_dic)
    status_dic = {}
    status_objs = await Status.objects.all()
    for status in status_objs:
        status_dic[status.name] = status.id
    db_notebooks = await Notebook.objects.select_related(['status']).filter(k8s_info__isnull=False).exclude(Notebook.status.name.startswith('stop')).all()
    bulk_update = False
    for nb in db_notebooks:
        name = nb.k8s_info.get('name')
        namespace = nb.k8s_info.get('namespace')
        obj = notebook_dic[f'{name}-{namespace}']
        if name and namespace and obj:
            bulk_update = True
            nb.url = obj['url']
            Notebook.compare_status_and_update(nb, obj['status'], status_dic)
    if bulk_update:
        await Notebook.objects.bulk_update(db_notebooks)


def job_listener(event):
    if event.exception:
        print("work exception")
    else:
        print("work worked!")


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # 后台
    # scheduler = BackgroundScheduler()
    # 阻塞，内存内显示
    # scheduler = BlockingScheduler()

    scheduler = AsyncIOScheduler()
    # todo 怎么从user的auth导入token
    # todo 考虑一直用一个管理员账号去login获取token?

    scheduler.add_job(job_func, trigger='interval', args=[1], id='1', name='a test job', max_instances=10,
                      jobstore='default', executor='default', seconds=10)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    print("sch start")
    scheduler.start()

# -*- coding: utf-8 -*-
"""
    >File   : scheduler_task.py
    >Auther : TXK
    >Mail   : xinkai.tao@digitalbrain.cn
    >Time   : 2022/12/22 18:55
"""

import asyncio
import logging
import ormar
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
    notebooks = await list_notebook_k8s(NoteBookListReq())
    notebook_dic = {}
    for notebook in notebooks:
        name = notebook['name']
        namespace = notebook['namespace']
        status = notebook['status']
        url = notebook['url']
        server_ip = notebook['server_ip']
        notebook_dic[f'{name}-{namespace}'] = {"status": status, 'url': url, 'server_ip': server_ip}
    print(notebook_dic)
    status_dic = {}
    status_objs = await Status.objects.all()
    for status in status_objs:
        status_dic[status.name] = status.id
    db_notebooks = await Notebook.objects.select_related(['status']).filter(k8s_info__isnull=False).exclude(
        Notebook.status.name.startswith('stop')).all()
    bulk_update = False
    for nb in db_notebooks:
        # 过滤脏数据
        if not nb.k8s_info:
            continue
        name = nb.k8s_info.get('name')
        namespace = nb.k8s_info.get('namespace')
        obj = notebook_dic.get(f'{name}-{namespace}') if name and namespace else None
        if name and namespace and obj:
            bulk_update = True
            nb.url = obj['url']
            nb.server_ip = obj['server_ip']
            Notebook.compare_status_and_update(nb, obj['status'], status_dic)
    if bulk_update:
        await Notebook.objects.bulk_update(db_notebooks)
    # 更新停止任务
    stop_notebooks = await Notebook.objects.select_related('status').filter(
        ormar.and_(k8s_info__isnull=False, status__name='stop')).all()
    stopped_status = await Status.objects.get(name='stopped')
    bulk_update = False
    for nb in stop_notebooks:
        # 过滤脏数据
        if not nb.k8s_info:
            continue
        name = nb.k8s_info.get('name')
        namespace = nb.k8s_info.get('namespace')
        obj = notebook_dic.get(f'{name}-{namespace}') if name and namespace else None
        if name and namespace and not obj:
            bulk_update = True
            nb.url = None
            nb.status = stopped_status
            nb.server_ip = obj['server_ip']
    if bulk_update:
        await Notebook.objects.bulk_update(stop_notebooks)


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

    scheduler.add_job(job_func, trigger='interval', args=[1], id='1', name='a test job', max_instances=10,
                      jobstore='default', executor='default', seconds=10)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    print("apscheduler start")
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

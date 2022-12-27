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


def job_func(job_id, token):
    print(f"job {job_id} run in {datetime.now()}")
    # todo 这里写刷新逻辑
    payloads = {}
    # 查询列表
    notebook_list = await list_notebook_k8s(token, payloads)

    stop_stat = await Status.objects.get(name='stop')
    stop_query = await Notebook.objects.filter(status=stop_stat).all()
    # todo 更新状态

    start_stat = await Status.objects.get(name='start')
    start_query = await Notebook.objects.filter(status=start_stat).all()
    # todo 更新状态


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

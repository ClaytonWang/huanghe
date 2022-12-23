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


def job_func(job_id):
    print(f"job {job_id} run in {datetime.now()}")


def job_listener(event):
    if event.exception:
        print("work exception")
    else:
        print("work worked!")


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # scheduler = BackgroundScheduler()
    # 阻塞，内存内显示
    # scheduler = BlockingScheduler()

    scheduler = AsyncIOScheduler()

    scheduler.add_job(job_func, trigger='interval', args=[1], id='1', name='a test job', max_instances=10,
                      jobstore='default', executor='default', seconds=10)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    print("sch start")
    scheduler.start()

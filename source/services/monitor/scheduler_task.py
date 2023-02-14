# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/10 15:23
@Auth ： Z01
@File ：scheduler_task.py
@Motto：You are the best!
"""
import asyncio
import logging
from datetime import datetime
from source.services.monitor.node.serializers import NodeCreate
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from models.initdb import startup_event
from k8s.cluster_client import cc

async def job_func(job_id):
    await startup_event()
    ncr=NodeCreate()
    await  cc.get_node_list(ncr)
    print(f"job {job_id} run in {datetime.now()}")


def job_listener(event):
    if event.exception:
        print("work exception")
    else:
        print("work worked!")


if __name__=='__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_func,trigger='interval',args=[1],id='1', name='a test job',max_instances=10,
                      jobstore='default',executor='default',seconds=5)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    print("apscheduler start")
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
import asyncio
import logging
from datetime import datetime
from servers.serializers import ServerCreateReq
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from models.initdb import startup_event
from models.server import Server

from utils.k8s_request import list_server_ip_k8s
from utils.service_requests import get_notebook_job_list_by_server


async def job_func(job_id):
    await startup_event()
    print(f"job {job_id} run in {datetime.now()}")
    serverlist = await  list_server_ip_k8s()
    for node in serverlist:
        ServerCreateReq.status = node['status']
        ServerCreateReq.server = node['serverIP']
        ServerCreateReq.cpu = node['cpu']
        ServerCreateReq.memory = node['memory']
        if node.get('gpu'):
            ServerCreateReq.gpu = node['gpu']
            ServerCreateReq.type = node['type']
        else:
            ServerCreateReq.gpu = 0
            ServerCreateReq.type = 'cpu'
        pod_list = await get_notebook_job_list_by_server(node['serverIP'])
        occupied_cpu = 0
        occupied_gpu = 0
        occupied_memory = 0
        occupied_user = []
        occupied_by = []
        for pod in pod_list:
            occupied_cpu += pod["cpu"]
            occupied_gpu += pod["gpu"]
            occupied_memory += pod["memory"]
            # print(f"node:{node['serverIP']} has:{pod}")
            if pod["created_by_id"] not in occupied_user:
                occupied_user.append(pod["created_by_id"])
                occupied_by.append({pod["created_by_id"]: pod["created_by"]})
        ServerCreateReq.occupied_cpu = occupied_cpu
        ServerCreateReq.occupied_gpu = occupied_gpu
        ServerCreateReq.occupied_memory = occupied_memory
        ServerCreateReq.occupied_by = occupied_by
        await Server.create_node_database(ServerCreateReq)


def job_listener(event):
    if event.exception:
        print("work exception")
    else:
        print("work worked!")


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_func, trigger='interval', args=[1], id='1', name='a test job', max_instances=10,
                      jobstore='default', executor='default', seconds=5)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    print("apscheduler start")
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

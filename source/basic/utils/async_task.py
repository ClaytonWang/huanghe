import asyncio
from types import coroutine


class AsyncTask:
    def __init__(self):
        self._task_list = []

    def add_task(self, task: coroutine):
        self._task_list.append(asyncio.create_task(task))

    async def run_tasks(self):
        return await asyncio.gather(*self._task_list)
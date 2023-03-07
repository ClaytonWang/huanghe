import ormar
from basic.common.initdb import DB, META
from asyncio import get_event_loop, ensure_future
import nest_asyncio
nest_asyncio.apply()



class Status(ormar.Model):
    class Meta(ormar.ModelMeta):
        tablename: str = "bam_status"
        metadata = META
        database = DB
        orders_by = ['-id']

    id: int = ormar.Integer(primary_key=True)
    code: str = ormar.String(max_length=20, comnet='状态码', unique=True)
    name: str = ormar.String(max_length=20, comnet='名称', unique=True)
    desc: str = ormar.String(max_length=40, comnet='描述')

    @classmethod
    async def all(cls):
        return await Status.objects.all()

    @classmethod
    async def status_cache(cls) -> dict:
        status_cache = {}
        a = await cls.all()
        for status_obj in a:
            status_cache[status_obj.name] = status_obj.id
        return status_cache

class StatusCache:
    def __init__(self):
        self.cache = {}

    def get(self, key, default=None):
        if not self.cache:
            self.cache = self.loader()
        return self.cache.get(key, default)

    def __getitem__(self, item):
        self.get(item)

    def loader(self):
        loop = get_event_loop()
        f = ensure_future(Status.status_cache())
        loop.run_until_complete(f)
        return f.result()

sc = StatusCache()
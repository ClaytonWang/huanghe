import logging
import time
import threading
from services.cluster.k8s.api.core import Core


# logging.basicConfig(
#     level=logging.INFO,
#     datefmt="%Y-%m-%d %H:%M:%S",
#     format="%(asctime)s %(levelname)s %(message)s",
# )


def Singleton(cls):
    cls._instance = None
    cls._lock = threading.RLock()

    def __new__(*args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = object.__new__(cls)
        return cls._instance

    cls.__new__ = __new__
    return cls


class K8sConfigFactory:
    @staticmethod
    def load_config(k8s):
        if k8s == 'huawei':
            return HuaweiConfig()
        elif k8s == 'zhongke':
            return ZKConfig()


@Singleton
class HuaweiConfig(Core):
    def __init__(self):
        hw_path = '~/.kube/config'
        super().__init__(path=hw_path)


@Singleton
class ZKConfig(Core):

    def __init__(self):
        zk_path = None
        super().__init__(path=zk_path)


# c = Core()
c = K8sConfigFactory.load_config('zhongke')
hw = K8sConfigFactory.load_config('huawei')

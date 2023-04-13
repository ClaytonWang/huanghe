import os
import random
import threading

import time
from kubernetes.config import load_kube_config, load_incluster_config
from kubernetes.client import CoreV1Api, CustomObjectsApi, StorageV1Api, AppsV1Api
from services.cluster.k8s.api.hw_v1beta1_api import HWV1Beta1Api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Core(FileSystemEventHandler):
    test="origin"
    def __init__(self, path=None,is_oberv=False):
        self._find_kubeconfig(path)
        self._core_v1_api = CoreV1Api()
        self._custom_object_api = CustomObjectsApi()
        self._storage_v1_api = StorageV1Api()
        self._apps_v1_api = AppsV1Api()
        self._v1_beta1_api = HWV1Beta1Api()
        self.observer = Observer()
        self.observer.unschedule_all()
        event_handler = self
        if is_oberv:
            self.observer.schedule(event_handler,
                                   path="./kubeconfig",
                                   recursive=False)
            self.thread = threading.Thread(target=self.observer.start)
            self.thread.start()

    def _find_kubeconfig(self, path=None):
        if path:
            load_kube_config(path)
        elif os.getenv("KUBECONFIG"):
            load_kube_config()
        else:
            load_incluster_config()
    def on_any_event(self, event):
        print("!!!!!!!!!!!modified!!!!!!!!!!!!    ")
        self.change()
        print("!!!!!!!!!!!modified!!!!!!!!!!!!    ")
    def change(self):
        print("!!!!!!!!!!!change!!!!!!!!!!!!    ")
        self.test = random.randint(0, 9999)
        print(self.test)

    @property
    def core_v1_api(self):
        return self._core_v1_api

    @property
    def custom_object_api(self):
        return self._custom_object_api

    @property
    def storage_v1_api(self):
        return self._storage_v1_api

    @property
    def apps_v1_api(self):
        return self._apps_v1_api

    @property
    def v1_beta1_api(self):
        return self._v1_beta1_api


kubeconfig_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "kubeconfig")


class K8sConfigFactory:
    pool = {}

    def __init__(self):
        if not self.pool:
            print("not pool")
            for file in os.listdir(kubeconfig_path):
                self.pool[file] = Core(os.path.join(kubeconfig_path, file))
        self.pool["default"] = Core()


    def __getitem__(self, item):
        if not item:
            return self.pool["default"]
        return self.pool[item]

    def get(self, key=None) -> Core:
        if not key:
            return self.pool["default"]
        return self.pool[key]

kcf = K8sConfigFactory()
print("create core end")

print("Event loop starting...")
class ExampleThread(threading.Thread):
    def __init__(self, obj, property):
        threading.Thread.__init__(self)
        self.obj = obj
        self.property = property


    def run(self):
        print("thread run")
        print(getattr(self.obj, self.property))
        print("done")
        # A.loop.run_forever()
        while True:
            print(getattr(self.obj, self.property))

            time.sleep(5)


print("thread start")
ExampleThread(kcf.pool["default"], "test").start()
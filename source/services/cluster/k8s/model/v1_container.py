from __future__ import annotations
from typing import Optional, List, Dict
from k8s.model.generic_mixin import GenericMixin
from k8s.model.v1_env_var import V1EnvVar
from k8s.model.v1_env_from_source import V1EnvFromSource
from k8s.model.v1_lifecycle import V1Lifecycle
from k8s.model.v1_probe import V1Probe
from k8s.model.v1_container_port import V1ContainerPort
from k8s.model.v1_resource_requirements import V1ResourceRequirements
from k8s.model.v1_volume_mount import V1VolumeMount


class V1Container(GenericMixin):
    args: Optional[List[str]]
    command: Optional[List[str]]
    env: Optional[List[V1EnvVar]] = []
    env_from: Optional[List[V1EnvFromSource]]
    image: str
    image_pull_policy: Optional[str]
    lifecycle: Optional[V1Lifecycle]
    liveness_probe: Optional[V1Probe]
    name: str
    ports: Optional[List[V1ContainerPort]]
    resources: Optional[V1ResourceRequirements]
    volume_mounts: Optional[List[V1VolumeMount]]
    working_dir: Optional[str]

    openapi_types = {
        'args': 'list[str]',
        'command': 'list[str]',
        'env': 'list[V1EnvVar]',
        'env_from': 'list[V1EnvFromSource]',
        'image': 'str',
        'image_pull_policy': 'str',
        'lifecycle': 'V1Lifecycle',
        'liveness_probe': 'V1Probe',
        'name': 'str',
        # 'ports': 'list[V1ContainerPort]',
        # 'readiness_probe': 'V1Probe',
        'resources': 'V1ResourceRequirements',
        # 'security_context': 'V1SecurityContext',
        # 'startup_probe': 'V1Probe',
        # 'stdin': 'bool',
        # 'stdin_once': 'bool',
        # 'termination_message_path': 'str',
        # 'termination_message_policy': 'str',
        # 'tty': 'bool',
        # 'volume_devices': 'list[V1VolumeDevice]',
        'volume_mounts': 'list[V1VolumeMount]',
        'working_dir': 'str'
    }

    attribute_map = {
        'args': 'args',
        'command': 'command',
        'env': 'env',
        'env_from': 'envFrom',
        'image': 'image',
        'image_pull_policy': 'imagePullPolicy',
        'lifecycle': 'lifecycle',
        'liveness_probe': 'livenessProbe',
        'name': 'name',
        'ports': 'ports',
        'readiness_probe': 'readinessProbe',
        'resources': 'resources',
        'security_context': 'securityContext',
        'startup_probe': 'startupProbe',
        'stdin': 'stdin',
        'stdin_once': 'stdinOnce',
        'termination_message_path': 'terminationMessagePath',
        'termination_message_policy': 'terminationMessagePolicy',
        'tty': 'tty',
        'volume_devices': 'volumeDevices',
        'volume_mounts': 'volumeMounts',
        'working_dir': 'workingDir',
    }

    def set_envs(self, envs: Dict[str, str]):
        self.env = [V1EnvVar.new(env_key, env_value) for env_key, env_value in envs.items()]
        return self

    def extend_envs(self, envs: Dict[str, str]):
        if not self.env:
            self.env = []
        self.env.extend([V1EnvVar.new(env_key, env_value) for env_key, env_value in envs.items()])
        return self

    def set_resources(self, requirements: Dict[str, str]):
        self.resources = V1ResourceRequirements.default(requirements=requirements)
        return self

    def set_volume_mounts(self, volume_mounts: List[Dict[str, str]]):
        self.volume_mounts = [V1VolumeMount.parse_obj(vm) for vm in volume_mounts]
        return self

    def extend_volume_mounts(self, volume_mounts: List[Dict[str, str]]):
        if not self.volume_mounts:
            self.volume_mounts = []
        self.volume_mounts.extend([V1VolumeMount.parse_obj(vm) for vm in volume_mounts])
        return self

    def extend_dshm_volume_mounts(self):
        if not self.volume_mounts:
            self.volume_mounts = []
        self.volume_mounts.extend([V1VolumeMount.default(name="dshm", mount_path="/dev/shm")])

    def set_image_pull_policy(self, image_pull_policy: str):
        self.image_pull_policy = image_pull_policy
        return self

    @classmethod
    def default(cls, name: str, image: str, command: List[str] = None, working_dir: Optional[str] = None):
        return cls.new(name=name, image=image, resources=None, command=command, working_dir=working_dir)

    @staticmethod
    def new(name: str, image: str, resources: Optional[V1ResourceRequirements], command: Optional[List[str]],
            working_dir: Optional[str]):
        return V1Container(name=name, image=image, resources=resources, command=command, working_dir=working_dir)

from __future__ import annotations
from typing import Optional, List, Dict
from model.generic_mixin import GenericMixin
from model.v1_env_var import V1EnvVar
from model.v1_env_from_source import V1EnvFromSource
from model.v1_lifecycle import V1Lifecycle
from model.v1_probe import V1Probe
from model.v1_container_port import V1ContainerPort

class V1Container(GenericMixin):
    args: Optional[List[str]]
    command: Optional[List[str]]
    env: Optional[List[V1EnvVar]]
    env_from: Optional[List[V1EnvFromSource]]
    image: str
    image_pull_policy: Optional[str]
    lifecycle: Optional[V1Lifecycle]
    liveness_probe: Optional[V1Probe]
    name: str
    ports: Optional[List[V1ContainerPort]]
    #

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
        # 'resources': 'V1ResourceRequirements',
        # 'security_context': 'V1SecurityContext',
        # 'startup_probe': 'V1Probe',
        # 'stdin': 'bool',
        # 'stdin_once': 'bool',
        # 'termination_message_path': 'str',
        # 'termination_message_policy': 'str',
        # 'tty': 'bool',
        # 'volume_devices': 'list[V1VolumeDevice]',
        # 'volume_mounts': 'list[V1VolumeMount]',
        # 'working_dir': 'str'
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

    def set_env(self, envs: Dict[str, str]):
        self.env = [V1EnvVar.new(env_key, env_value) for env_key, env_value in envs.items()]
        return self

    def set_resources(self):
        return self

    @staticmethod
    def new(name: str, image: str):
        return V1Container(name=name, image=image, command=["sleep 50000"])
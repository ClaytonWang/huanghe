from source.services.cluster.k8s.model.v1_container import V1Container
from services.cluster.k8s.model.v1_env_var import V1EnvVar
from services.cluster.k8s.model.v1_resource_requirements import V1ResourceRequirements
from services.cluster.k8s.model.v1_volume_mount import V1VolumeMount


def compare_dicts(d1, d2):
    """
    递归比较两个字典是否相等
    """
    if isinstance(d1, dict) and isinstance(d2, dict):
        if d1.keys() != d2.keys():
            return False
        for key in d1.keys():
            if not compare_dicts(d1[key], d2[key]):
                return False
        return True
    else:
        return d1 == d2

class TestV1Container:

    def test_set_envs(self):
        container = V1Container.default(name="container", image="test-image")
        envs = {"KEY1": "value1"}
        container.set_envs(envs)
        for env in container.env:
            assert getattr(env, 'name') == "KEY1"
            assert getattr(env,  'value') == "value1"
        # assert container.env.name="KEY1"



    def test_extend_envs(self):
        container = V1Container.default(name="container", image="test-image")
        envs = {"KEY1": "value1", "KEY2": "value2"}
        container.extend_envs(envs)
        assert container.env == [V1EnvVar.new("KEY1", "value1"), V1EnvVar.new("KEY2", "value2")]
        container.extend_envs(envs)
        assert container.env == [V1EnvVar.new("KEY1", "value1"), V1EnvVar.new("KEY2", "value2"),V1EnvVar.new("KEY1", "value1"), V1EnvVar.new("KEY2", "value2")]

    def test_set_resources(self):
        container = V1Container.default(name="container", image="test-image")
        requirements = {"cpu": "500m", "memory": "512Mi"}
        container.set_resources(requirements)
        assert container.resources == V1ResourceRequirements.default(requirements=requirements)

    def test_set_volume_mounts(self):
        container = V1Container.default(name="container", image="test-image")
        volume_mounts = [{"name": "data", "mount_path": "/data"}, {"name": "config", "mount_path": "/config"}]
        container.set_volume_mounts(volume_mounts)
        assert container.volume_mounts == [V1VolumeMount.parse_obj(vm) for vm in volume_mounts]

    def test_extend_volume_mounts(self):
        container = V1Container.default(name="container", image="test-image")
        volume_mounts = [{"name": "data", "mount_path": "/data"}, {"name": "config", "mount_path": "/config"}]
        container.extend_volume_mounts(volume_mounts)
        assert container.volume_mounts == [V1VolumeMount.parse_obj(vm) for vm in volume_mounts]

        container2 = V1Container.default(name="container2", image="test-image")
        container2.extend_volume_mounts(volume_mounts)
        assert container2.volume_mounts == [V1VolumeMount.parse_obj(vm) for vm in volume_mounts]

    def test_extend_dshm_volume_mounts(self):
        container = V1Container.default(name="container", image="test-image")
        container.extend_dshm_volume_mounts()
        assert container.volume_mounts == [V1VolumeMount.default(name="dshm", mount_path="/dev/shm")]

    def test_set_image_pull_policy(self):
        container = V1Container.default(name="container", image="test-image")
        container.set_image_pull_policy("Always")
        assert container.image_pull_policy == "Always"

    def test_default(self):
        name = "container"
        image = "test-image"
        command = ["echo", "hello"]
        working_dir = "/app"
        container = V1Container.default(name=name, image=image, command=command, working_dir=working_dir)
        assert container.name == name
        assert container.image == image
        assert container.command == command
        assert container.working_dir == working_dir

from pytest import fixture
from services.cluster.k8s.model.v1_pod_spec import V1PodSpec


@fixture()
def pod_spec():
    return V1PodSpec.default(name="pod_spec", image="test-image")


def test_add_pvc_volume_and_volume_mount(pod_spec):
    from source.services.cluster.notebook.serializers import Volume
    volume1 = Volume(name="vol1",mount_path = "dev/")
    volume2 = Volume(name="vol2", mount_path="dev/")
    volumes = [volume1,volume2]
    pod_spec.add_pvc_volume_and_volume_mount(volumes)
    print(pod_spec.volumes[0])



def test_add_dshm(pod_spec):
    pod_spec.add_dshm()
    assert pod_spec.volumes[0].name=='dshm'
    assert pod_spec.containers[0].volume_mounts[0].mount_path == '/dev/shm'


def test_add_tolerations(pod_spec):
    tolerations = ['key1=value1:NoSchedule', 'key2=value2:NoSchedule']
    pod_spec.add_tolerations(tolerations)
    assert pod_spec.tolerations[0].operator=='Exists'


def test_add_image_pull_secrets(pod_spec):
    secrets = ['secret1', 'secret2']
    pod_spec.add_image_pull_secrets(secrets)
    assert pod_spec.image_pull_secrets[1].name == 'secret2'


def test_set_restart_policy(pod_spec):
    restart_policy = 'OnFailure'
    pod_spec.set_restart_policy(restart_policy)
    assert pod_spec.restart_policy == restart_policy


def test_default(pod_spec):
    name, image = 'test_name', 'test_image'
    result = V1PodSpec.default(name, image)
    assert result.containers[0].name == name
    assert result.containers[0].image == image




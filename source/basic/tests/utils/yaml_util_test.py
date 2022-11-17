import unittest

from utils.yaml_util import convert_yaml_to_dict


class TestYamlUtil(unittest.TestCase):
    def setUp(self) -> None:
        self.check = {'apiVersion': 'apps/v1', 'kind': 'Deployment',
                      'metadata': {'generateName': 'example-pod-', 'namespace': 'default', 'labels': {'app': 'example-pod'}},
                      'spec': {'replicas': 1, 'strategy': {'type': 'Recreate'}, 'selector': {'matchLabels': {'app': 'example-pod'}},
                               'template': {'metadata': {'labels': {'app': 'example-pod'}}, 'spec': {'containers': [
                                   {'name': 'example-pod-container', 'image': 'busybox', 'imagePullPolicy': 'IfNotPresent',
                                    'command': ['/bin/bash', '-c', '--'], 'args': ['while true; do sleep 30; done;'],
                                       'ports': [{'containerPort': 10000, 'protocol': 'TCP'}]}], 'restartPolicy': 'Always',
                                   'nodeName': 'node-name'}}}}

    def test_convert_yaml_to_dict(self):
        result = convert_yaml_to_dict("../yaml_config/example.yaml")
        self.assertDictEqual(result, self.check)

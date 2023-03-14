from source.services.cluster.k8s.model.v1_resource_requirements import V1ResourceRequirements
class TestV1ResourceRequirements:

    def test_default(self):
        requirements = {'cpu': '100m', 'memory': '128Mi'}
        expected = {'limits': {'cpu': '100m', 'memory': '128Mi'},
                    'requests': {'cpu': '100m', 'memory': '128Mi'}}
        assert V1ResourceRequirements.default(requirements).to_dict() == expected

    def test_only_requests_storage(self):
        size = '1'
        expected = {'limits': None, 'requests': {'storage': '1Gi'}}
        assert V1ResourceRequirements.only_requests_storage(size).to_dict() == expected

    def test_new(self):
        limits = {'cpu': '500m'}
        requests = {'cpu': '200m', 'memory': '256Mi'}
        expected = {'limits': {'cpu': '500m'}, 'requests': {'cpu': '200m', 'memory': '256Mi'}}
        assert V1ResourceRequirements.new(limits, requests).to_dict() == expected

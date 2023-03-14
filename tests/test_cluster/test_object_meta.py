from services.cluster.k8s.model.v1_object_meta import V1ObjectMeta

class TestV1ObjectMeta:
    @classmethod
    def setup_class(cls):
        cls.name = "test-object"
        cls.namespace = "default"
        cls.annotations = {"key": "value"}
        cls.labels = {"app": "test"}

    def test_without_istio_injection(self):
        meta = V1ObjectMeta.without_istio_injection(self.name, self.namespace, self.annotations, self.labels)
        assert meta.name == self.name
        assert meta.namespace == self.namespace
        assert meta.annotations == {"key": "value", "sidecar.istio.io/inject": "false"}
        assert meta.labels == {"app": "test"}

    def test_new(self):
        meta = V1ObjectMeta.new(self.name, self.namespace, self.annotations, self.labels)
        assert meta.name == self.name
        assert meta.namespace == self.namespace
        assert meta.annotations == self.annotations
        assert meta.labels == self.labels
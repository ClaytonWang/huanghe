from source.services.cluster.k8s.model.v1_pod import V1Pod





def test_pod():
    p = V1Pod.default("ss", "test", "test")
    assert p.kind == "Pod"


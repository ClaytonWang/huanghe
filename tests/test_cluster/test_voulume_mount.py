from services.cluster.k8s.model.v1_volume_mount import V1VolumeMount


class TestV1VolumeMount:

    def test_default(self):
        name = "test-name"
        mount_path = "/test/mount/path"
        expected = {
            'mount_path': '/test/mount/path',
            'name': 'test-name',
            'read_only': None,
            'sub_path': None,
            'sub_path_expr': None,
            'mount_propagation': None
        }
        assert V1VolumeMount.default(name, mount_path).to_dict() == expected

    def test_new(self):
        name = "test-name"
        mount_path = "/test/mount/path"
        mount_propagation = "test-propagation"
        sub_path = "test-sub-path"
        sub_path_expr = "test-sub-path-expr"
        read_only = True
        expected = {
        'mount_path': '/test/mount/path',
        'name': 'test-name',
        'read_only': True,
        'sub_path': 'test-sub-path',
        'sub_path_expr': 'test-sub-path-expr',
        'mount_propagation': "test-propagation"
        }
        assert V1VolumeMount.new(name, mount_path, mount_propagation, sub_path, sub_path_expr, read_only).to_dict() == expected


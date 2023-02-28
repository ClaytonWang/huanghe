from source.services.cluster.k8s.model.v1_alpha1_volcano_job import V1Alpha1VolcanoJob


def test_vcjob():
    vj = V1Alpha1VolcanoJob.default(name="test",
                                    namespace="ns",
                                    image="aaa",
                                    labels=[],
                                    resource={"cpu": 1, "memory": 1},
                                    envs={},
                                    volumes=[],
                                    tolerations=[],
                                    command=["sleep 5000"],
                                    working_dir="/root",
                                    annotations={})
    assert vj.kind == "Job"


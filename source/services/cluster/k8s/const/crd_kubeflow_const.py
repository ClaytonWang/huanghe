KUBEFLOW_V1_API_VERSION = "kubeflow.org/v1"

VOLCANO_V1_ALPHA1_API_VERSION = "batch.volcano.sh/v1alpha1"

KUBEFLOW_V1_VERSION = "v1"

VOLCANO_V1_ALPHA1_VERSION = "v1alpha1"

KUBEFLOW_NOTEBOOK_KIND = "Notebook"

KUBEFLOW_SERVICE_KIND = "Service"

VOLCANO_JOB_KIND = "Job"

KUBEFLOW_NOTEBOOK_GROUP = "kubeflow.org"

VOLCANO_JOB_GROUP = "batch.volcano.sh"

KUBEFLOW_NOTEBOOK_PLURAL = "notebooks"

VOLCANO_JOB_PLURAL = "jobs"

VOLCANO_DEFAULT_QUEUE = "default"

VOLCANO_DEFAULT_MAX_RETRY = 3

VOLCANO_DEFAULT_MIN_AVAILABLE = 1

VOLCANO_TASK_REPLICAS = 1

VOLCANO_TASK_DEFAULT_NAME = "tfjob"

VOLCANO_TASK_MASTER_NAME = "mpimaster"

VOLCANO_TASK_WORKER_NAME = "mpiworker"

TENSORFLOW_PLUGIN = {"tensorflow": ["--port=5000", "--worker=worker", "--ps=ps"]}

PYTORCH_PLUGIN = {"pytorch": ["--master=master","--worker=worker", "--port=23456"]}

MPI_PLUGIN = {"mpi": ["--master=master", "--worker=worker", "--port=22"]}

DEEPSPEED_PLUGIN = {"deepspeed": ["--master=master", "--worker=worker", "--port=22"]}

TENSORFLOW_MODE = "tensorflow"

PYTORCH_MODE = "pytorch"

MPI_MODE = "mpi"

DEEPSPEED_MODE = "deepspeed"

POLICY_TASK_COMPLETED_EVENT_TO_COMPLETE_JOB_ACTION = {"action": "CompleteJob", "event": "TaskCompleted"}

ISTIO_DISABLE_INJECT_ANNOTATION = {"sidecar.istio.io/inject": "false"}

HUAWEICLOUD_GPU_NAMESPACE_ANNOTATION = {"namespace.kubernetes.io/flavor": "gpu-accelerated"}

HUAWEICLOUD_CPU_NAMESPACE_ANNOTATION = {"namespace.kubernetes.io/flavor": "general-computing"}

HUAWEICLOUD_NETWORK_ANNOTATION = {"network.alpha.kubernetes.io/domain-id": "a13b3c35734648b39befee62731ae42f",
                                  "network.alpha.kubernetes.io/default-security-group":"6664c5b1-294c-4078-8153-cd07b5437683",
                                  "network.alpha.kubernetes.io/project-id": "9c2349a364784c38a4e40121ef5d67d4",}

HUAWEICLOUD_ENTERPRISE_PROJECT_LABEL = "sys_enterprise_project_id"

HUAWEICLOUD_INGRESS_APIVERSION = "extensions/v1beta1"

HUAWEICLOUD_INGRESS_KIND = "Ingress"

HUAWEICLOUD_NETWORK_APIVERSION = "networking.cci.io/v1beta1"

HUAWEICLOUD_NETWORK_KIND = "Network"

HUAWEICLOUD_NETWORK_AVAILABLE_ZONE = "cn-north-4a"

HUAWEICLOUD_NETWORK_CIDR = "192.168.0.0/18"

HUAWEICLOUD_NETWORK_VPC_ID = "c4bfbd62-44e9-4b6c-9629-613e892ce4f2"

HUAWEICLOUD_NETWORK_SUBNET_ID = "516e5c43-f315-469a-bf47-cd68fc49e819"

HUAWEICLOUD_NETWORK_NETWORK_ID = "828770d8-4d8b-4ab8-8b70-07c8ab8fc0e3"

HUAWEICLOUD_NETWORK_NETTYPE = "underlay_neutron"
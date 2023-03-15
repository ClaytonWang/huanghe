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

TENSORFLOW_PLUGIN = {"tensorflow": ["--port=5000", "--worker=worker", "--ps=ps"]}

PYTORCH_PLUGIN = {"pytorch": ["--master=master","--worker=worker","--port=23456"]}

TENSORFLOW_MODE = "tensorflow"

PYTORCH_MODE = "pytorch"

ISTIO_DISABLE_INJECT_ANNOTATION = {"sidecar.istio.io/inject": "false"}

HUAWEICLOUD_GPU_NAMESPACE_ANNOTATION = {"namespace.kubernetes.io/flavor": "gpu-accelerated"}

HUAWEICLOUD_CPU_NAMESPACE_ANNOTATION = {"namespace.kubernetes.io/flavor": "general-computing"}

HUAWEICLOUD_ENTERPRISE_PROJECT_LABEL = "sys_enterprise_project_id"
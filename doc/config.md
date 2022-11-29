### Doc
[微服务](../README.md)

## 配置

**k8s configmap挂载到容器中**

[k8s.configmap doc](https://kubernetes.io/docs/concepts/configuration/configmap/)

配置使用configmap命名 **service-config**

**configmap 配置文件样例**

第一层为服务名

```yaml
# configmap
apiVersion: v1
kind: ConfigMap
metadata:
  name: service-config
  namespace: juece
data:
  user: |
    PYTHON_ENV: production
    SERVICE_NAME: user
```

约定统一挂载路径 **/config/juece/config.yaml**

**微服务容器中挂载的 配置文件样例**
```yaml
PYTHON_ENV: production
SERVICE_NAME: user
```

### 服务读取配置样例(python)

```python
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("/config/juece/config.yaml", "r") as stream:
  data = load(stream, Loader=Loader)
  print(data)

# stdout
# {'PYTHON_ENV': 'production', 'SERVICE_NAME': 'user'}
```

### 配置实践建议
1. 代码应考虑 **配置文件不存在** 的情况，**配置项应有默认值**
2. **只提取需要的配置项**，如环境相关、租户相关等需要动态配置的配置项。其他服务内部的配置项（比如为勒收口，方便集中管理），建议服务内部另有配置模块处理。

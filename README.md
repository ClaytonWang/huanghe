### Doc
[配置](/doc/config.md)

## 微服务模块

| 微服务      | 对应模块       | 服务说明            |
|----------|------------|-----------------|
| frontend | 前端         | 前端服务            |
| user     | 用户管理       | 用户、认证、鉴权服务      |
| cluster  | 集群管理       | k8s对接           |
| storages | 存储管理       | 持久化存储管理         |
| notebook | notebook管理 | 管理notebook生命周期  |
| monitor  | 总览管理       | 总览资源、开发统计、服务器监控 |

**微服务间调用**
```bash
# Example: Http方式调用user微服务
curl $USER_SERVICE_HOST:$USER_SERVICE_PORT
```

**服务配置说明**

[服务配置](doc/config.md)

**微服务模块架构**

![架构图](doc/source/architecture.jpeg)
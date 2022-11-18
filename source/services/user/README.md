![这是图片](pic/digitalbrain_image.png "Magic Gardens")
# FastAPI 模版项目
## 简介:
### 这是一个基于FastAPI的，轻量，可直接运行的后端服务器项目的基础接口和项目模版。
### 启动./start_service.sh后，可实时编辑工程代码，自动文档和后端代码都会较快动态加载。
### 开发过程中无需重启服务器，实时更新功能。

---
### 运行工程:
### virtualenv venv
### source venv/bin/activate
### pip install -r requirements.txt
### ./start_service.sh
### 查看本地自动文档 http://localhost:5000/redoc

---
### 非调试时后台守护进程运行:
### ./start_service_daemon.sh
### 需要手动kill，仅用于脱离temrinal交互环境，实际生产环境部署还是需要Dockerfile打包等严肃的部署方案
### nohup uvicorn main:app --host 0.0.0.0 --port 5000 --reload  > log.txt 2>&1 &

---
![这是图片](pic/fastapi_image.png "Magic Gardens")
### FastAPI documentation
### https://fastapi.tiangolo.com/

---
### http 库相关
### https://www.python-httpx.org/

---
### data model 封装数据obj、数据传输obj相关
### https://docs.python.org/3.8/library/dataclasses.html
### https://pydantic-docs.helpmanual.io/

---
### unit test 库相关
### https://docs.python.org/3/library/unittest.html

---
### 如何使用自动文档:
### ip:port/redoc  example: http://123.60.89.88:5000/redoc

---
### redis 封装:
### controller/redis_controller.py

---
### grpc和protobuf生成文件夹、shell脚本:
### data_model/protos
### protobuf、python3.6+ dataclass等对应的数据对象封装:
### data_model/task_dto.py

---
### 接口单元测试 (todo: 和测试小伙伴对一下自动化接口测试的代码)
### test/api_test/*_test.py

---
### controller控制层单元测试
### controller/*_test.py

---
### utils单元测试
### utils/*_test.py

---
### PostgreSQL 批量读写和对象
### utils/psql_connection_util.py

---
### 数据批处理和ETL处理的pandas扩展对象
### etl/dto_process.py

---
### python kubernetes库example，可直接通过其中函数操作k8s环境:
### k8s_operator/examples

---
### Ormar 异步ORM框架
[官方文档](https://alembic.sqlalchemy.org/en/latest/)

---
### - Alembic 数据库迁移工具
  - alembic init alembic 在项目根目录初始化迁移环境 
    1. 初始化结束需要更新env.py里的target_metadata，保持和项目的一致
    2. 设置alembic.ini 的sqlalchemy.url
  - alembic revision --autogenerate -m "made some changes" 生成迁移文件
  - alembic upgrade head 更新数据库 
  - alembic downgrade head 回滚迁移

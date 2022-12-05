
--- 
### 环境 `virtualenv` 或是 `conda`:


--- 
### 依赖 `requirements.txt`
安装依赖 `pip install -r requirements.txt`

### 执行服务 `python main.py` 默认端口是 `8000`

--- 
### 接口文档参考 `apifox` 或是自带的 `/docs`

---
### [配置参考](doc/config.md) 的`服务使用配置说明`

---
### Ormar 异步ORM框架
[官方文档](https://alembic.sqlalchemy.org/en/latest/)

--- 
### 数据验证和格式化输出 `pydantic`

---
### - 数据库迁移工具 `Alembic`
  - alembic init alembic 在项目根目录初始化迁移环境 
    1. 初始化结束需要更新env.py里的target_metadata，保持和项目的一致
    2. 设置alembic.ini 的sqlalchemy.url
  - alembic revision --autogenerate -m "made some changes" 生成迁移文件
  - alembic upgrade head 更新数据库 
  - alembic downgrade head 回滚迁移

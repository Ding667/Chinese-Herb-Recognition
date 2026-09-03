# -*- coding: utf-8 -*-
# MySQL 数据库连接配置
import os

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": os.environ.get("DB_PASSWORD", "123456"),  # 本地开发默认；生产环境请通过 .env 覆盖
    "database": "herb_recognition",
    "charset": "utf8mb4",
}

# -*- coding: utf-8 -*-
"""MySQL 数据存储模块（历史记录 + 用户）"""
from datetime import datetime

import pymysql

from app.config import DB_CONFIG
from app.security import hash_password


def _conn(with_db=True):
    cfg = dict(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        charset=DB_CONFIG["charset"],
    )
    if with_db:
        cfg["database"] = DB_CONFIG["database"]
    return pymysql.connect(**cfg)


def init_db():
    """创建数据库与数据表"""
    conn = _conn(with_db=False)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8mb4"
                % DB_CONFIG["database"]
            )
        conn.commit()
    finally:
        conn.close()

    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS detection_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    image_name VARCHAR(64) NOT NULL,
                    result_image VARCHAR(64) NOT NULL,
                    target_count INT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at DATETIME NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        conn.commit()
    finally:
        conn.close()

    init_users_table()


def init_users_table():
    """创建用户表，并预置默认管理员账号 admin"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(64) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    created_time DATETIME NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        conn.commit()
    finally:
        conn.close()
    # 预置默认管理员（admin / admin123），密码以哈希形式存储
    if find_user_by_name("admin") is None:
        create_user("admin", hash_password("admin123"))


def create_user(username, password_hash):
    """创建用户；用户名已存在返回 False，成功返回 True"""
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM users WHERE username = %s", (username,)
            )
            if cur.fetchone():
                return False
            cur.execute(
                "INSERT INTO users (username, password, created_time) "
                "VALUES (%s, %s, %s)",
                (
                    username,
                    password_hash,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
        conn.commit()
        return True
    finally:
        conn.close()


def find_user_by_name(username):
    """按用户名查询用户，返回 dict 或 None"""
    conn = _conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                "SELECT id, username, password FROM users "
                "WHERE username = %s",
                (username,),
            )
            return cur.fetchone()
    finally:
        conn.close()


def save_history(image_name, result_image, target_count, result_json):
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO detection_history "
                "(image_name, result_image, target_count, result_json, created_at) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    image_name,
                    result_image,
                    target_count,
                    result_json,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
        conn.commit()
    finally:
        conn.close()


def list_history(limit=50):
    conn = _conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                "SELECT id, image_name, result_image, target_count, "
                "result_json, created_at FROM detection_history "
                "ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
            for r in rows:
                if isinstance(r["created_at"], datetime):
                    r["created_at"] = r["created_at"].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            return rows
    finally:
        conn.close()


def delete_history(record_id):
    conn = _conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM detection_history WHERE id = %s", (record_id,))
        conn.commit()
    finally:
        conn.close()

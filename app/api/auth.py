# -*- coding: utf-8 -*-
"""用户注册与登录接口"""
from fastapi import APIRouter
from pydantic import BaseModel

from app.db import create_user, find_user_by_name
from app.security import hash_password, verify_password

router = APIRouter()


class UserIn(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user: UserIn):
    """用户注册：校验用户名唯一性，密码加密存储"""
    username = user.username.strip()
    password = user.password
    if not username or not password:
        return {"code": 400, "message": "用户名和密码不能为空"}
    if len(username) > 32 or len(password) > 64:
        return {"code": 400, "message": "用户名或密码长度不合法"}
    if find_user_by_name(username):
        return {"code": 400, "message": "用户名已存在"}
    if not create_user(username, hash_password(password)):
        return {"code": 400, "message": "用户名已存在"}
    return {"code": 200, "message": "注册成功"}


@router.post("/login")
async def login(user: UserIn):
    """用户登录：校验用户名与密码"""
    username = user.username.strip()
    if not username or not user.password:
        return {"code": 400, "message": "用户名和密码不能为空"}
    row = find_user_by_name(username)
    if row is None or not verify_password(user.password, row["password"]):
        return {"code": 400, "message": "用户名或密码错误"}
    return {"code": 200, "message": "登录成功", "data": {"username": username}}

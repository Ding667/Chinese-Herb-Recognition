# -*- coding: utf-8 -*-
"""密码加密工具：sha256 + 随机盐（不引入额外依赖）"""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """生成密码哈希，格式：salt$digest"""
    salt = secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    """校验明文密码与存储哈希是否匹配"""
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest() == digest

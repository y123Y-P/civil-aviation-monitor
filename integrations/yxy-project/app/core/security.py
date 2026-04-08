# 文件名:integrations/yxy-project/app/core/security.py
# 功能:security 相关实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\core\security.py
功能: 安全认证
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import jwt
import bcrypt

from app.core.config import settings

_BCRYPT_ROUNDS = 12


def get_password_hash(password: str) -> str:
    """
    直接使用 bcrypt 库生成 hash。

    说明：当前环境中 passlib[bcrypt] 与 bcrypt 版本存在兼容问题，
    直接改用 bcrypt 可避免启动/注册/登录时的哈希失败。
    """
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except Exception:
        return False


def create_access_token(*, subject: str, expires_delta: timedelta | None = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": subject,  # 这里用 username 作为 subject（后续也可扩展为 user_id）
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    返回 JWT payload。
    由上层处理异常（如 expired / invalid）。
    """

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={"verify_aud": False},
    )


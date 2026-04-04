from __future__ import annotations

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginIn, RegisterIn
from app.services.user_service import create_user, get_user_by_email, get_user_by_username
import app.services.rbac_service as rbac_service


def register(db: Session, data: RegisterIn) -> User:
    existing = get_user_by_username(db, data.username)
    if existing is not None:
        # 暂时直接抛出异常，后续统一错误处理/响应格式再完善
        raise ValueError("username already exists")

    existing_email = get_user_by_email(db, str(data.email))
    if existing_email is not None:
        raise ValueError("email already exists")

    user = create_user(
        db,
        username=data.username,
        email=str(data.email),
        password=data.password,
        nickname=data.nickname,
        avatar=data.avatar,
        is_superuser=False,
    )

    # 注册时绑定角色（限制普通注册角色，reviewer/admin 由后台分配）
    allowed_register_roles = {"normal_user", "author"}
    role_code = (data.role_code or "normal_user").strip()
    if role_code not in allowed_register_roles:
        raise ValueError(f"role not allowed for registration: {role_code}")

    # 绑定角色（幂等：如果角色不存在/数据未迁移好会抛异常）
    rbac_service.assign_roles_to_user(db, user=user, role_codes=[role_code])
    db.refresh(user)
    return user


def login(db: Session, data: LoginIn) -> tuple[str, User]:
    user = get_user_by_username(db, data.username)
    if user is None:
        raise ValueError("user not found")

    if user.status != User.STATUS_ACTIVE:
        raise ValueError("user is disabled")

    if not verify_password(data.password, user.password_hash):
        raise ValueError("invalid credentials")

    access_token = create_access_token(
        subject=user.username,
    )
    return access_token, user


def get_token_subject(token_payload: dict) -> str:
    subject = token_payload.get("sub")
    if not subject:
        raise JWTError("missing sub")
    return str(subject)


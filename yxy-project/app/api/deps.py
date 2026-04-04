from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user_service import get_user_by_username
from app.services.rbac_service import user_has_permission, user_has_role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


# 直接复用 core/database 的依赖生成器
get_db_dep = get_db


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_dep),
) -> User:
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = get_user_by_username(db, str(username))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.status != User.STATUS_ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
        )
    return current_user


async def get_optional_current_user(
    token: str | None = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db_dep),
) -> User | None:
    """
    给“公开接口”使用：未携带 token 时返回 None；携带 token 但无效则仍返回 401。
    """
    if not token:
        return None

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = get_user_by_username(db, str(username))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if user.status != User.STATUS_ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
        )
    return user


def require_role(role_code: str):
    """
    用于路由级别的角色校验依赖。
    - admin / is_superuser 直接放行
    """

    async def _dependency(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db_dep),
    ) -> User:
        if current_user.is_superuser:
            return current_user
        if user_has_role(db, current_user.id, "admin"):
            return current_user
        if user_has_role(db, current_user.id, role_code):
            return current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough role")

    return _dependency


def require_permission(permission_code: str):
    """
    用于路由级别的权限校验依赖。
    - admin / is_superuser 直接放行（这里用 is_superuser 做直通）
    """

    async def _dependency(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db_dep),
    ) -> User:
        if current_user.is_superuser:
            return current_user
        if user_has_role(db, current_user.id, "admin"):
            return current_user
        if user_has_permission(db, current_user.id, permission_code):
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permission",
        )

    return _dependency


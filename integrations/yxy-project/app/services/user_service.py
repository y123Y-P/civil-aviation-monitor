# 文件名:integrations/yxy-project/app/services/user_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\user_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_password_hash


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalars().first()


def create_user(
    db: Session,
    *,
    username: str,
    email: str,
    password: str,
    nickname: str | None = None,
    avatar: str | None = None,
    is_superuser: bool = False,
) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        nickname=nickname,
        avatar=avatar,
        is_superuser=is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


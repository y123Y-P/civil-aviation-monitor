# 文件名:yxy-project/app/services/role_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\role_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


def get_role_by_code(db: Session, code: str) -> Role | None:
    stmt = select(Role).where(Role.code == code)
    return db.execute(stmt).scalars().first()


def list_roles(db: Session) -> list[Role]:
    stmt = select(Role).order_by(Role.id.asc())
    return list(db.execute(stmt).scalars().all())


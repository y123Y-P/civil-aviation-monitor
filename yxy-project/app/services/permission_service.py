from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission


def get_permission_by_code(db: Session, code: str) -> Permission | None:
    stmt = select(Permission).where(Permission.code == code)
    return db.execute(stmt).scalars().first()


def list_permissions(db: Session) -> list[Permission]:
    stmt = select(Permission).order_by(Permission.id.asc())
    return list(db.execute(stmt).scalars().all())


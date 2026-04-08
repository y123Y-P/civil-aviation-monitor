# 文件名:yxy-project/app/services/rbac_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\rbac_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole
from app.models.user import User
from app.services.permission_service import get_permission_by_code
from app.services.role_service import get_role_by_code


def get_user_roles(db: Session, user_id: int) -> list[Role]:
    stmt = (
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
    )
    return list(db.execute(stmt).scalars().all())


def get_user_permissions(db: Session, user_id: int) -> list[Permission]:
    """
    查询用户的全部权限（通过 user_roles -> role_permissions）。
    """
    stmt = (
        select(Permission)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .where(UserRole.user_id == user_id)
    )
    return list(db.execute(stmt).scalars().all())


def user_has_role(db: Session, user_id: int, role_code: str) -> bool:
    stmt = (
        select(Role.id)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id, Role.code == role_code)
    )
    return db.execute(stmt).first() is not None


def user_has_permission(db: Session, user_id: int, permission_code: str) -> bool:
    stmt = (
        select(Permission.id)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .where(UserRole.user_id == user_id, Permission.code == permission_code)
    )
    return db.execute(stmt).first() is not None


def assign_roles_to_user(db: Session, *, user: User, role_codes: list[str]) -> list[Role]:
    """
    给用户绑定角色，避免重复绑定。
    """
    if not role_codes:
        return []

    # 去重但保留顺序不重要
    uniq_codes = list(dict.fromkeys(role_codes))

    existing_role_ids = {
        rid for (rid,) in db.execute(
            select(UserRole.role_id).where(UserRole.user_id == user.id)
        ).all()
    }

    roles_to_add: list[Role] = []
    for code in uniq_codes:
        role = get_role_by_code(db, code)
        if role is None:
            raise ValueError(f"role not found: {code}")
        if role.id in existing_role_ids:
            continue
        roles_to_add.append(role)

    for role in roles_to_add:
        db.add(UserRole(user_id=user.id, role_id=role.id))

    db.commit()

    # 返回最终角色集合
    return get_user_roles(db, user.id)


def get_user_permission_codes(db: Session, user_id: int) -> list[str]:
    perms = get_user_permissions(db, user_id)
    return [p.code for p in perms]


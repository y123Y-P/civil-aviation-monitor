# 文件名:integrations/yxy-project/app/seeds/rbac_seed.py
# 功能:rbac_seed 相关实现
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole


@dataclass(frozen=True)
class PermissionSeed:
    name: str
    code: str
    description: str


@dataclass(frozen=True)
class RoleSeed:
    name: str
    code: str
    description: str
    permission_codes: list[str]


DEFAULT_PERMISSIONS: list[PermissionSeed] = [
    # user
    PermissionSeed("用户查看", "user:read", "查看用户信息"),
    PermissionSeed("用户更新", "user:update", "更新用户信息"),
    # article
    PermissionSeed("文章创建", "article:create", "创建文章"),
    PermissionSeed("文章读取", "article:read", "读取文章"),
    PermissionSeed("文章更新", "article:update", "更新文章草稿/内容"),
    PermissionSeed("文章删除", "article:delete", "删除文章"),
    PermissionSeed("提交审核", "article:submit_review", "提交审核"),
    PermissionSeed("发布文章", "article:publish", "发布文章"),
    PermissionSeed("下架文章", "article:offline", "下架文章"),
    # review
    PermissionSeed("审核读取", "review:read", "读取审核记录/待审列表"),
    PermissionSeed("审核通过", "review:approve", "审核通过"),
    PermissionSeed("审核驳回", "review:reject", "审核驳回"),
    # category/tag/event management
    PermissionSeed("分类管理", "category:manage", "管理分类"),
    PermissionSeed("标签管理", "tag:manage", "管理标签"),
    PermissionSeed("事件管理", "event:manage", "管理事件"),
    # generation (预留)
    PermissionSeed("生成创建", "generation:create", "创建生成任务"),
    PermissionSeed("生成读取", "generation:read", "读取生成结果"),
    PermissionSeed("生成管理", "generation:manage", "管理生成任务/结果"),
]


DEFAULT_ROLES: list[RoleSeed] = [
    RoleSeed(
        "普通用户",
        "normal_user",
        "浏览公开内容",
        ["user:read", "article:read"],
    ),
    RoleSeed(
        "作者/博主",
        "author",
        "创建/编辑并提交审核自己的内容",
        ["user:read", "article:read", "article:create", "article:update", "article:submit_review"],
    ),
    RoleSeed(
        "审核/管理用户",
        "reviewer",
        "审核文章并管理资源",
        [
            "user:read",
            "article:read",
            "article:create",
            "article:update",
            "article:publish",
            "article:offline",
            "review:read",
            "review:approve",
            "review:reject",
            "category:manage",
            "tag:manage",
            "event:manage",
            "generation:create",
            "generation:read",
            "generation:manage",
        ],
    ),
    # admin 预留：拥有全部权限（由 seed 统一绑定）
    RoleSeed(
        "超级管理员",
        "admin",
        "拥有全部权限（或通过 is_superuser 直通）",
        [],
    ),
]


def _ensure_permissions(db: Session, permissions: Iterable[PermissionSeed]) -> dict[str, Permission]:
    created: dict[str, Permission] = {}
    for p in permissions:
        existing = db.execute(select(Permission).where(Permission.code == p.code)).scalars().first()
        if existing is None:
            existing = Permission(name=p.name, code=p.code, description=p.description)
            db.add(existing)
            db.commit()
            db.refresh(existing)
        created[p.code] = existing
    return created


def _ensure_roles(db: Session, roles: Iterable[RoleSeed]) -> dict[str, Role]:
    created: dict[str, Role] = {}
    for r in roles:
        existing = db.execute(select(Role).where(Role.code == r.code)).scalars().first()
        if existing is None:
            existing = Role(name=r.name, code=r.code, description=r.description)
            db.add(existing)
            db.commit()
            db.refresh(existing)
        created[r.code] = existing
    return created


def _ensure_role_permissions(
    db: Session, *, role: Role, permission_ids: list[int]
) -> None:
    if not permission_ids:
        return
    existing = db.execute(
        select(RolePermission.permission_id).where(RolePermission.role_id == role.id)
    ).scalars().all()
    existing_set = set(existing)
    to_add = [pid for pid in permission_ids if pid not in existing_set]
    for pid in to_add:
        db.add(RolePermission(role_id=role.id, permission_id=pid))
    if to_add:
        db.commit()


def seed_rbac(db: Session) -> None:
    """
    初始化默认 RBAC 数据（幂等）。
    注意：需要在对应表完成迁移后执行；如果表不存在会抛 OperationalError。
    """

    permissions = _ensure_permissions(db, DEFAULT_PERMISSIONS)
    roles = _ensure_roles(db, DEFAULT_ROLES)

    # admin 拥有全部权限
    admin_role = roles.get("admin")
    if admin_role:
        all_permission_ids = [p.id for p in permissions.values()]
        _ensure_role_permissions(db, role=admin_role, permission_ids=all_permission_ids)

    for role_seed in DEFAULT_ROLES:
        if role_seed.code == "admin":
            continue
        role = roles[role_seed.code]
        permission_ids = [permissions[code].id for code in role_seed.permission_codes if code in permissions]
        _ensure_role_permissions(db, role=role, permission_ids=permission_ids)


def safe_seed_rbac(db: Session) -> None:
    """
    容错 seed：当表不存在或连接失败时不致使服务启动失败。
    """

    try:
        seed_rbac(db)
    except OperationalError:
        # 未迁移导致表不存在等情况：跳过
        db.rollback()
    except IntegrityError:
        db.rollback()


# 文件名:integrations/yxy-project/app/models/user.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\models\user.py
功能: 数据模型定义
"""
from __future__ import annotations

from sqlalchemy import Boolean, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class User(BaseModel):
    """
    用户表模型（基础版）

    说明：
    - username / email 唯一
    - password_hash 不对外暴露
    - status 先提供 active / disabled
    - is_superuser 预留给后续 RBAC/后台能力
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    # 注意：MySQL utf8mb4 下 UNIQUE 索引的最大 key length 会因服务器参数而更严格。
    # 你当前环境在 VARCHAR(191) 创建唯一索引时仍报 1071，
    # 因此这里进一步保守收敛，避免迁移/建表失败。
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar: Mapped[str | None] = mapped_column(String(512), nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        CheckConstraint("status in ('active','disabled')", name="ck_users_status"),
    )

    # 常量：方便业务层判断
    STATUS_ACTIVE = "active"
    STATUS_DISABLED = "disabled"


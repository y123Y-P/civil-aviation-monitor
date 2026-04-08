# 文件名:integrations/yxy-project/app/schemas/role.py
# 功能:数据模型与结构定义
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AssignRolesIn(BaseModel):
    user_id: int
    role_codes: list[str]


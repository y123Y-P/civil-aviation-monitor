from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

from .permission import PermissionOut
from .role import RoleOut

class UserBase(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    status: str
    is_superuser: bool = False


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserMeOut(UserOut):
    """
    只是语义区分：/users/me 的返回用户结构
    """


class UserPermissionsOut(UserMeOut):
    """
    /users/me/permissions 返回结构（包含 roles/permissions）
    """

    roles: list[RoleOut] = []
    permissions: list[PermissionOut] = []



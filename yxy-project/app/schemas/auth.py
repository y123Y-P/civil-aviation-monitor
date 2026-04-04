from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr

from .user import UserOut


class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    # 注册时选择角色（预留：后续可扩展为多角色）
    # 普通用户注册仅允许 normal_user/author；reviewer/admin 由后台分配。
    role_code: str = "normal_user"


class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserOut] = None


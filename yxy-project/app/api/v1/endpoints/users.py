# 文件名:yxy-project/app/api/v1/endpoints/users.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\api\v1\endpoints\users.py
功能: API接口定义
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.schemas.user import UserMeOut, UserPermissionsOut
from app.core.database import get_db
import app.services.rbac_service as rbac_service

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserMeOut)
async def me(current_user=Depends(get_current_active_user)):
    return current_user


@router.get("/me/permissions", response_model=UserPermissionsOut)
async def me_permissions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    roles = rbac_service.get_user_roles(db, current_user.id)
    permissions = rbac_service.get_user_permissions(db, current_user.id)
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "avatar": current_user.avatar,
        "status": current_user.status,
        "is_superuser": current_user.is_superuser,
        # response_model 里 UserOut 继承链路要求 created_at/updated_at
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
        "roles": roles,
        "permissions": permissions,
    }


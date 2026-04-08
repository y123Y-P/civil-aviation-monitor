# 文件名:yxy-project/app/api/v1/endpoints/roles.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\api\v1\endpoints\roles.py
功能: API接口定义
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.core.database import get_db
from app.schemas.role import AssignRolesIn, RoleOut
import app.services.rbac_service as rbac_service
import app.services.role_service as role_service


router = APIRouter(tags=["roles"])


@router.get("", response_model=list[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("admin")),
):
    roles = role_service.list_roles(db)
    return roles


@router.post("/assign", response_model=list[RoleOut])
def assign_roles(
    payload: AssignRolesIn,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("admin")),
):
    # 复用 rbac_service 中的绑定逻辑
    from app.models.user import User

    user = db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    try:
        roles = rbac_service.assign_roles_to_user(db, user=user, role_codes=payload.role_codes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return roles


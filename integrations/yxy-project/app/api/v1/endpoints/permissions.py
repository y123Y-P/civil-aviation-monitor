# 文件名:integrations/yxy-project/app/api/v1/endpoints/permissions.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\api\v1\endpoints\permissions.py
功能: API接口定义
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.core.database import get_db
from app.schemas.permission import PermissionOut
import app.services.permission_service as permission_service


router = APIRouter(tags=["permissions"])


@router.get("", response_model=list[PermissionOut])
def list_permissions(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("admin")),
):
    perms = permission_service.list_permissions(db)
    return perms


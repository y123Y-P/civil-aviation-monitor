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


# 文件名:integrations/yxy-project/app/api/v1/endpoints/tags.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\api\v1\endpoints\tags.py
功能: API接口定义
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_optional_current_user, require_permission
from app.core.database import get_db
from app.schemas.tag import TagCreate, TagListItem, TagRead, TagUpdate
import app.services.tag_service as tag_service
import app.services.article_relation_service as article_relation_service
import app.services.rbac_service as rbac_service

router = APIRouter(tags=["tags"])


def _is_admin_like(current_user, db: Session) -> bool:
    if current_user is None:
        return False
    return (
        current_user.is_superuser
        or rbac_service.user_has_role(db, current_user.id, "admin")
        or rbac_service.user_has_role(db, current_user.id, "reviewer")
    )


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    payload: TagCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("tag:manage")),
):
    try:
        return tag_service.create_tag(db, data=payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def list_tags(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("user:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    keyword: str | None = Query(default=None),
):
    items, total = tag_service.list_tags(db, page=page, page_size=page_size, keyword=keyword)
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("user:read")),
):
    tag = tag_service.get_tag_by_id(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    payload: TagUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("tag:manage")),
):
    tag = tag_service.get_tag_by_id(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    try:
        return tag_service.update_tag(db, tag=tag, data=payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("tag:manage")),
):
    tag = tag_service.get_tag_by_id(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="tag not found")
    tag_service.delete_tag(db, tag=tag)
    return None


@router.get("/{tag_id}/articles")
def list_tag_articles(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
):
    if not tag_service.get_tag_by_id(db, tag_id):
        raise HTTPException(status_code=404, detail="tag not found")

    is_admin = _is_admin_like(current_user, db)
    items, total = article_relation_service.list_articles_by_tag(
        db,
        tag_id=tag_id,
        is_admin=is_admin,
        page=page,
        page_size=page_size,
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


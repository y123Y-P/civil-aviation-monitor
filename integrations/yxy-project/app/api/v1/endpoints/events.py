# 文件名:integrations/yxy-project/app/api/v1/endpoints/events.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\api\v1\endpoints\events.py
功能: API接口定义
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_current_active_user, get_optional_current_user, require_permission
from app.core.database import get_db
from app.schemas.event import EventCreate, EventListItem, EventRead, EventUpdate
import app.services.event_service as event_service
import app.services.article_relation_service as article_relation_service
import app.services.rbac_service as rbac_service

router = APIRouter(tags=["events"])


def _is_admin_like(current_user, db: Session) -> bool:
    if current_user is None:
        return False
    return (
        current_user.is_superuser
        or rbac_service.user_has_role(db, current_user.id, "admin")
        or rbac_service.user_has_role(db, current_user.id, "reviewer")
    )


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("event:manage")),
):
    try:
        return event_service.create_event(db, created_by=current_user.id, data=payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def list_events(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("user:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    keyword: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    items, total = event_service.list_events(
        db, page=page, page_size=page_size, keyword=keyword, status=status
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{event_id}", response_model=EventRead)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("user:read")),
):
    event = event_service.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="event not found")
    return event


@router.put("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int,
    payload: EventUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("event:manage")),
):
    event = event_service.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="event not found")
    try:
        return event_service.update_event(db, event=event, data=payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("event:manage")),
):
    event = event_service.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="event not found")
    event_service.delete_event(db, event=event)
    return None


@router.get("/{event_id}/articles")
def list_event_articles(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
):
    if not event_service.get_event_by_id(db, event_id):
        raise HTTPException(status_code=404, detail="event not found")

    is_admin = _is_admin_like(current_user, db)
    items, total = article_relation_service.list_articles_by_event(
        db,
        event_id=event_id,
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


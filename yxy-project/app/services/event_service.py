# 文件名:yxy-project/app/services/event_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\event_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate
from app.utils.slug import slugify


def get_event_by_id(db: Session, event_id: int) -> Event | None:
    stmt = select(Event).where(Event.id == event_id)
    return db.execute(stmt).scalars().first()


def list_events(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    status: str | None = None,
) -> tuple[list[Event], int]:
    offset = (page - 1) * page_size
    stmt = select(Event).order_by(Event.id.desc())
    count_stmt = select(Event.id)

    filters = []
    if keyword:
        kw = f"%{keyword.strip()}%"
        filters.append((Event.title.like(kw)) | (Event.summary.like(kw)))
    if status:
        filters.append(Event.status == status)

    if filters:
        stmt = stmt.where(*filters)
        count_stmt = count_stmt.where(*filters)

    total = db.execute(count_stmt).all()
    total_count = len(total)
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())
    return items, total_count


def create_event(db: Session, *, created_by: int, data: EventCreate) -> Event:
    base_slug = data.slug or slugify(data.title)
    slug = base_slug
    idx = 1
    while db.execute(select(Event.id).where(Event.slug == slug)).first() is not None:
        idx += 1
        slug = f"{base_slug}-{idx}"

    event = Event(
        title=data.title,
        slug=slug,
        summary=data.summary,
        description=data.description,
        status=data.status,
        source_url=data.source_url,
        happened_at=data.happened_at,
        created_by=created_by,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, *, event: Event, data: EventUpdate) -> Event:
    payload = data.model_dump(exclude_none=True)
    for k, v in payload.items():
        setattr(event, k, v)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, *, event: Event) -> None:
    db.delete(event)
    db.commit()


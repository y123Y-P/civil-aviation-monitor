# 文件名:integrations/yxy-project/app/services/tag_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\tag_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate
from app.utils.slug import slugify


def get_tag_by_id(db: Session, tag_id: int) -> Tag | None:
    stmt = select(Tag).where(Tag.id == tag_id)
    return db.execute(stmt).scalars().first()


def list_tags(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
) -> tuple[list[Tag], int]:
    offset = (page - 1) * page_size
    stmt = select(Tag).order_by(Tag.id.desc())
    count_stmt = select(Tag.id)

    if keyword:
        kw = f"%{keyword.strip()}%"
        stmt = stmt.where(Tag.name.like(kw))
        count_stmt = count_stmt.where(Tag.name.like(kw))

    total = db.execute(count_stmt).all()
    total_count = len(total)
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())
    return items, total_count


def create_tag(db: Session, *, data: TagCreate) -> Tag:
    base_slug = data.slug or slugify(data.name)
    slug = base_slug
    idx = 1
    while db.execute(select(Tag.id).where(Tag.slug == slug)).first() is not None:
        idx += 1
        slug = f"{base_slug}-{idx}"

    tag = Tag(
        name=data.name,
        slug=slug,
        description=data.description,
    )
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def update_tag(db: Session, *, tag: Tag, data: TagUpdate) -> Tag:
    payload = data.model_dump(exclude_none=True)
    if "name" in payload and payload["name"] is not None:
        tag.name = payload["name"]
    if "slug" in payload and payload["slug"]:
        tag.slug = payload["slug"]
    if "description" in payload:
        tag.description = payload["description"]

    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, *, tag: Tag) -> None:
    db.delete(tag)
    db.commit()


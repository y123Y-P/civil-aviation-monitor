# 文件名:yxy-project/app/services/draft_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\draft_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article_draft import ArticleDraft
from app.schemas.draft import DraftCreate, DraftUpdate


def create_draft(db: Session, *, author_id: int, data: DraftCreate) -> ArticleDraft:
    draft = ArticleDraft(
        title=data.title,
        summary=data.summary,
        cover_image=data.cover_image,
        content=data.content,
        author_id=author_id,
        source_type=data.source_type,
        source_url=data.source_url,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


def get_draft_by_id(db: Session, draft_id: int) -> ArticleDraft | None:
    stmt = select(ArticleDraft).where(ArticleDraft.id == draft_id)
    return db.execute(stmt).scalars().first()


def list_drafts(
    db: Session,
    *,
    author_id: int | None = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple[list[ArticleDraft], int]:
    stmt = select(ArticleDraft).order_by(ArticleDraft.id.desc())
    count_stmt = select(ArticleDraft.id)

    if author_id is not None:
        stmt = stmt.where(ArticleDraft.author_id == author_id)
        count_stmt = count_stmt.where(ArticleDraft.author_id == author_id)

    total = db.execute(count_stmt).all()
    total_count = len(total)
    items = list(db.execute(stmt.limit(limit).offset(offset)).scalars().all())
    return items, total_count


def update_draft(db: Session, *, draft: ArticleDraft, data: DraftUpdate) -> ArticleDraft:
    # 仅更新非 None 字段
    payload = data.model_dump(exclude_none=True)
    for k, v in payload.items():
        setattr(draft, k, v)

    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


def delete_draft(db: Session, *, draft: ArticleDraft) -> None:
    db.delete(draft)
    db.commit()


from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete, or_, select
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.article_event import ArticleEvent
from app.models.article_tag import ArticleTag
from app.models.category import Category
from app.models.event import Event
from app.models.tag import Tag


def set_article_category(
    db: Session, *, article: Article, category_id: int | None
) -> Article:
    if category_id is not None:
        category = db.execute(select(Category).where(Category.id == category_id)).scalars().first()
        if category is None:
            raise ValueError("category not found")
    article.category_id = category_id
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def replace_article_tags(db: Session, *, article: Article, tag_ids: list[int]) -> None:
    # 验证 tag 是否存在
    if tag_ids:
        tags = db.execute(select(Tag).where(Tag.id.in_(tag_ids))).scalars().all()
        found_ids = {t.id for t in tags}
        missing = [tid for tid in tag_ids if tid not in found_ids]
        if missing:
            raise ValueError(f"tag not found: {missing[0]}")

    # 删除旧关系（替换式更新）
    db.execute(delete(ArticleTag).where(ArticleTag.article_id == article.id))
    db.commit()

    unique_ids = list(dict.fromkeys(tag_ids))
    for tid in unique_ids:
        db.add(ArticleTag(article_id=article.id, tag_id=tid))
    db.commit()


def replace_article_events(db: Session, *, article: Article, event_ids: list[int]) -> None:
    if event_ids:
        events = db.execute(select(Event).where(Event.id.in_(event_ids))).scalars().all()
        found_ids = {e.id for e in events}
        missing = [eid for eid in event_ids if eid not in found_ids]
        if missing:
            raise ValueError(f"event not found: {missing[0]}")

    db.execute(delete(ArticleEvent).where(ArticleEvent.article_id == article.id))
    db.commit()

    unique_ids = list(dict.fromkeys(event_ids))
    for eid in unique_ids:
        db.add(ArticleEvent(article_id=article.id, event_id=eid))
    db.commit()


def _list_articles_base(
    db: Session,
    *,
    stmt,
    page: int,
    page_size: int,
) -> tuple[list[Article], int]:
    offset = (page - 1) * page_size
    count_stmt = stmt.with_only_columns(Article.id).order_by(None)
    total = len(db.execute(count_stmt).all())
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())

    # 兼容“通过审核但尚未 publish”的历史数据：
    # 若 status=approved 但 published_at 为空，前端可能按 published_at 判定可见性。
    # 这里只做响应归一化，不落库。
    for a in items:
        if a.status == "approved" and a.published_at is None:
            a.published_at = datetime.now(timezone.utc)
    return items, total


def list_articles_by_category(
    db: Session,
    *,
    category_id: int,
    current_user_id: int | None,
    is_admin: bool,
    page: int,
    page_size: int,
    keyword: str | None = None,
) -> tuple[list[Article], int]:
    stmt = select(Article).where(Article.category_id == category_id).order_by(Article.id.desc())
    if not is_admin:
        stmt = stmt.where(Article.status.in_(["published", "approved"]))
    if keyword:
        kw = f"%{keyword.strip()}%"
        stmt = stmt.where(or_(Article.title.like(kw), Article.summary.like(kw)))
    return _list_articles_base(db, stmt=stmt, page=page, page_size=page_size)


def list_articles_by_tag(
    db: Session,
    *,
    tag_id: int,
    is_admin: bool,
    page: int,
    page_size: int,
) -> tuple[list[Article], int]:
    stmt = (
        select(Article)
        .join(ArticleTag, ArticleTag.article_id == Article.id)
        .where(ArticleTag.tag_id == tag_id)
        .order_by(Article.id.desc())
    )
    if not is_admin:
        stmt = stmt.where(Article.status.in_(["published", "approved"]))
    return _list_articles_base(db, stmt=stmt, page=page, page_size=page_size)


def list_articles_by_event(
    db: Session,
    *,
    event_id: int,
    is_admin: bool,
    page: int,
    page_size: int,
) -> tuple[list[Article], int]:
    stmt = (
        select(Article)
        .join(ArticleEvent, ArticleEvent.article_id == Article.id)
        .where(ArticleEvent.event_id == event_id)
        .order_by(Article.id.desc())
    )
    if not is_admin:
        stmt = stmt.where(Article.status.in_(["published", "approved"]))
    return _list_articles_base(db, stmt=stmt, page=page, page_size=page_size)


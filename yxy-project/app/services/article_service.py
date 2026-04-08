# 文件名:yxy-project/app/services/article_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\article_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.utils.slug import slugify


def _ensure_unique_slug(db: Session, base_slug: str, article_id: int | None = None) -> str:
    """
    保证 slug 唯一。
    - article_id 仅在更新时用于排除当前文章的 slug 冲突。
    """

    slug = base_slug
    idx = 1
    while True:
        stmt = select(Article.id).where(Article.slug == slug)
        if article_id is not None:
            stmt = stmt.where(Article.id != article_id)
        exists = db.execute(stmt).first()
        if exists is None:
            return slug
        idx += 1
        slug = f"{base_slug}-{idx}"


def create_article(db: Session, *, author_id: int, data: ArticleCreate, status: str = "draft") -> Article:
    base_slug = slugify(data.title)
    final_slug = _ensure_unique_slug(db, base_slug)

    article = Article(
        title=data.title,
        slug=final_slug,
        summary=data.summary,
        cover_image=data.cover_image,
        content=data.content,
        category_id=data.category_id,
        status=status,
        author_id=author_id,
        source_type=data.source_type,
        source_url=data.source_url,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article_by_id(db: Session, article_id: int) -> Article | None:
    stmt = select(Article).where(Article.id == article_id)
    return db.execute(stmt).scalars().first()


def list_articles(
    db: Session,
    *,
    author_id: int | None = None,
    status: str | list[str] | None = None,
    keyword: str | None = None,
    limit: int = 10,
    offset: int = 0,
) -> tuple[list[Article], int]:
    stmt = select(Article).order_by(Article.id.desc())
    count_stmt = select(Article.id)

    filters = []
    if author_id is not None:
        filters.append(Article.author_id == author_id)
    if status is not None:
        if isinstance(status, list):
            filters.append(Article.status.in_(status))
        else:
            filters.append(Article.status == status)
    if keyword:
        kw = f"%{keyword.strip()}%"
        filters.append(or_(Article.title.like(kw), Article.summary.like(kw)))

    if filters:
        stmt = stmt.where(and_(*filters))
        count_stmt = count_stmt.where(and_(*filters))

    # 轻量分页：先取 id 再 count
    total = db.execute(count_stmt).all()
    total_count = len(total)
    items = list(db.execute(stmt.limit(limit).offset(offset)).scalars().all())
    return items, total_count


def update_article(db: Session, *, article: Article, data: ArticleUpdate) -> Article:
    payload = data.model_dump(exclude_none=True)

    # title 变更时同步 slug
    new_title = payload.get("title")
    if new_title and new_title != article.title:
        base_slug = slugify(str(new_title))
        article.slug = _ensure_unique_slug(db, base_slug, article_id=article.id)

    for k, v in payload.items():
        if k == "title":
            article.title = v
            continue
        setattr(article, k, v)

    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, *, article: Article) -> None:
    db.delete(article)
    db.commit()


def submit_for_review(_db: Session, *, article_id: int) -> None:
    """
    后续审核流转预留入口：本轮不暴露完整接口，只保留 service 层扩展点。
    """
    return


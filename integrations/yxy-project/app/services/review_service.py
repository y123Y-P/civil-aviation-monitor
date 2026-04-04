from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.article_draft import ArticleDraft
from app.models.review_record import ReviewRecord
from app.schemas.review import ReviewRejectRequest
from app.services.article_workflow_service import validate_transition
import app.services.article_service as article_service
from app.schemas.article import ArticleCreate


def get_draft_by_id(db: Session, draft_id: int) -> ArticleDraft | None:
    return db.execute(select(ArticleDraft).where(ArticleDraft.id == draft_id)).scalars().first()


def get_article_by_id(db: Session, article_id: int) -> Article | None:
    return db.execute(select(Article).where(Article.id == article_id)).scalars().first()


def _apply_draft_to_article_fields(*, draft: ArticleDraft, article: Article) -> None:
    """
    只做字段应用，不做状态机校验与提交；由上层统一控制提交时机。
    """
    article.title = draft.title
    article.summary = draft.summary
    article.cover_image = draft.cover_image
    article.content = draft.content
    article.status = "pending_review"

    # 草稿不带分类信息，本轮不改文章 category_id
    article.source_type = draft.source_type
    article.source_url = draft.source_url
    article.published_at = None  # 进入审核流程时清空发布时间


def submit_draft_for_review(
    db: Session,
    *,
    draft: ArticleDraft,
    article: Article | None,
    submitter_id: int,
) -> tuple[Article, ReviewRecord]:
    from_status = article.status if article is not None else "draft"
    to_status = validate_transition(from_status, action="submit")  # pending_review

    if article is None:
        create_data = ArticleCreate(
            title=draft.title,
            summary=draft.summary,
            cover_image=draft.cover_image,
            content=draft.content,
            category_id=None,
            status="draft",
            source_type=draft.source_type,
            source_url=draft.source_url,
        )
        article = article_service.create_article(
            db,
            author_id=draft.author_id,
            data=create_data,
            status="pending_review",
        )
    else:
        # 已存在 article：先校验状态机，再同步内容并进入待审核
        _apply_draft_to_article_fields(draft=draft, article=article)
        db.add(article)
        db.commit()
        db.refresh(article)

    # 如果草稿已有 related_article_id，直接复用；否则回写
    if draft.related_article_id != article.id:
        draft.related_article_id = article.id
        db.add(draft)
        db.commit()
        db.refresh(draft)

    # 保证到达目标状态（一般已是 pending_review）
    if article.status != to_status:
        article.status = to_status
        article.published_at = None
        db.add(article)
        db.commit()
        db.refresh(article)

    review = ReviewRecord(
        article_id=article.id,
        draft_id=draft.id,
        reviewer_id=submitter_id,
        action="submit",
        from_status=from_status,
        to_status=article.status,
        comment=None,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return article, review


def submit_article_for_review(
    db: Session,
    *,
    article: Article,
    submitter_id: int,
) -> ReviewRecord:
    from_status = article.status
    to_status = validate_transition(from_status, action="submit")

    article.status = to_status
    if to_status != "published":
        article.published_at = None
    db.add(article)
    db.commit()
    db.refresh(article)

    review = ReviewRecord(
        article_id=article.id,
        draft_id=None,
        reviewer_id=submitter_id,
        action="submit",
        from_status=from_status,
        to_status=to_status,
        comment=None,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def approve_article(db: Session, *, article: Article, reviewer_id: int) -> ReviewRecord:
    from_status = article.status
    to_status = validate_transition(from_status, action="approve")
    article.status = to_status
    # UI/展示层可能把 `published_at` 作为“已通过/可见”的判定条件之一。
    # 在进入 approved 时同步发布时间，保证“通过审核后对所有人可见”。
    if to_status == "approved":
        article.published_at = datetime.now(timezone.utc)
    db.add(article)
    db.commit()
    db.refresh(article)

    review = ReviewRecord(
        article_id=article.id,
        draft_id=None,
        reviewer_id=reviewer_id,
        action="approve",
        from_status=from_status,
        to_status=to_status,
        comment=None,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def reject_article(
    db: Session,
    *,
    article: Article,
    reviewer_id: int,
    request: ReviewRejectRequest,
) -> ReviewRecord:
    from_status = article.status
    to_status = validate_transition(from_status, action="reject")
    article.status = to_status
    article.published_at = None
    db.add(article)
    db.commit()
    db.refresh(article)

    review = ReviewRecord(
        article_id=article.id,
        draft_id=None,
        reviewer_id=reviewer_id,
        action="reject",
        from_status=from_status,
        to_status=to_status,
        comment=request.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def publish_article(db: Session, *, article: Article, reviewer_id: int) -> ReviewRecord:
    from_status = article.status
    to_status = validate_transition(from_status, action="publish")
    article.status = to_status
    article.published_at = datetime.now(timezone.utc)
    db.add(article)
    db.commit()
    db.refresh(article)

    review = ReviewRecord(
        article_id=article.id,
        draft_id=None,
        reviewer_id=reviewer_id,
        action="publish",
        from_status=from_status,
        to_status=to_status,
        comment=None,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def offline_article(db: Session, *, article: Article, reviewer_id: int) -> ReviewRecord:
    from_status = article.status
    to_status = validate_transition(from_status, action="offline")
    article.status = to_status
    db.add(article)
    db.commit()
    db.refresh(article)

    review = ReviewRecord(
        article_id=article.id,
        draft_id=None,
        reviewer_id=reviewer_id,
        action="offline",
        from_status=from_status,
        to_status=to_status,
        comment=None,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def list_pending_articles(db: Session, *, page: int, page_size: int, keyword: str | None = None) -> tuple[list[Article], int]:
    offset = (page - 1) * page_size
    stmt = select(Article).where(Article.status == "pending_review").order_by(Article.id.desc())
    count_stmt = select(Article.id).where(Article.status == "pending_review")
    if keyword:
        kw = f"%{keyword.strip()}%"
        stmt = stmt.where((Article.title.like(kw)) | (Article.summary.like(kw)))
        count_stmt = count_stmt.where((Article.title.like(kw)) | (Article.summary.like(kw)))
    total = len(db.execute(count_stmt).all())
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())
    return items, total


def list_review_records_by_article(db: Session, *, article_id: int, page: int, page_size: int) -> tuple[list[ReviewRecord], int]:
    offset = (page - 1) * page_size
    stmt = select(ReviewRecord).where(ReviewRecord.article_id == article_id).order_by(ReviewRecord.created_at.desc())
    count_stmt = select(ReviewRecord.id).where(ReviewRecord.article_id == article_id)
    total = len(db.execute(count_stmt).all())
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())
    return items, total


def list_review_history(
    db: Session,
    *,
    page: int,
    page_size: int,
    action: str | None = None,
    to_status: str | None = None,
    reviewer_id: int | None = None,
    keyword: str | None = None,
) -> tuple[list[ReviewRecord], int]:
    offset = (page - 1) * page_size
    stmt = select(ReviewRecord).order_by(ReviewRecord.created_at.desc())
    count_stmt = select(ReviewRecord.id)

    filters = []
    if action:
        filters.append(ReviewRecord.action == action)
    if to_status:
        filters.append(ReviewRecord.to_status == to_status)
    if reviewer_id is not None:
        filters.append(ReviewRecord.reviewer_id == reviewer_id)
    if keyword:
        kw = f"%{keyword.strip()}%"
        # 关键字优先在 comment 上做轻量过滤
        filters.append(ReviewRecord.comment.like(kw))

    if filters:
        stmt = stmt.where(*filters)
        count_stmt = count_stmt.where(*filters)

    total = len(db.execute(count_stmt).all())
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())
    return items, total


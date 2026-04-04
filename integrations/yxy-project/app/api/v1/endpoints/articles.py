from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_optional_current_user, require_permission
from app.core.database import get_db
from app.schemas.article import (
    ArticleCreate,
    ArticlePageResponse,
    ArticleRead,
    ArticleUpdate,
    ArticleCategoryUpdate,
    ArticleEventsUpdate,
    ArticleTagsUpdate,
)
import app.services.article_service as article_service
import app.services.rbac_service as rbac_service
import app.services.article_relation_service as article_relation_service

router = APIRouter(tags=["articles"])


def _is_reviewer_or_admin(current_user, db: Session) -> bool:
    return (
        current_user.is_superuser
        or rbac_service.user_has_role(db, current_user.id, "reviewer")
        or rbac_service.user_has_role(db, current_user.id, "admin")
    )


@router.post("", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(
    payload: ArticleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:create")),
):
    # 文章先进入 draft 状态（本轮不做复杂审核流转）
    return article_service.create_article(db, author_id=current_user.id, data=payload, status="draft")


@router.get("", response_model=ArticlePageResponse)
def list_articles(
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    status: str | None = Query(default=None, description="过滤状态（reviewer/admin 可用）"),
    author_id: int | None = Query(default=None, description="过滤作者（reviewer/admin 可用）"),
    keyword: str | None = Query(default=None, description="标题/摘要关键词（轻量）"),
    mine: bool = Query(default=False, description="仅查看自己的文章"),
):
    limit = page_size
    offset = (page - 1) * page_size

    is_admin = current_user is not None and _is_reviewer_or_admin(current_user, db)

    # 非管理员用户：默认只查看已发布内容；mine=true 则查看自己的所有状态
    effective_author_id = author_id
    effective_status = status

    if not is_admin:
        if mine:
            if current_user is None:
                raise HTTPException(status_code=401, detail="not authenticated")
            # mine=true：查看自己的所有状态（含 draft/pending_review 等）
            effective_author_id = current_user.id
            effective_status = None
        else:
            # mine=false 且未指定 author_id：查看“所有作者的已发布文章”
            # 让 effective_author_id 保持为传入参数（默认 None），由 service 层决定是否过滤作者。
            effective_author_id = author_id
            # 这里把“通过审核”的 approved 也当作公开状态（与前端的“审核通过”口径一致）
            effective_status = ["published", "approved"]
    else:
        if mine:
            # admin/mine 需要登录用户存在
            if current_user is None:
                raise HTTPException(status_code=401, detail="not authenticated")
            effective_author_id = current_user.id

    items, total = article_service.list_articles(
        db,
        author_id=effective_author_id,
        status=effective_status,
        keyword=keyword,
        limit=limit,
        offset=offset,
    )

    # 兼容“approved但published_at为空”的历史数据：
    # 统一在响应层补齐，避免前端按 published_at 判断可见性时出现空列表。
    for a in items:
        if a.status == "approved" and a.published_at is None:
            a.published_at = datetime.now(timezone.utc)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
):
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_owner = current_user is not None and article.author_id == current_user.id
    is_admin = current_user is not None and _is_reviewer_or_admin(current_user, db)

    # draft/pending_review 等仅作者或审核/管理员可见；approved/published 允许公开查看
    if article.status not in {"published", "approved"} and not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="not enough permission")

    # 兼容“approved但published_at为空”的历史数据：保证响应中 published_at 非空
    if article.status == "approved" and article.published_at is None:
        article.published_at = datetime.now(timezone.utc)

    return article


@router.put("/{article_id}", response_model=ArticleRead)
def update_article(
    article_id: int,
    payload: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:update")),
):
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_owner = article.author_id == current_user.id
    is_admin = _is_reviewer_or_admin(current_user, db)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="not enough permission")

    return article_service.update_article(db, article=article, data=payload)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:delete")),
):
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_owner = article.author_id == current_user.id
    is_admin = _is_reviewer_or_admin(current_user, db)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="not enough permission")

    article_service.delete_article(db, article=article)
    return None


@router.get("/me/list", response_model=ArticlePageResponse)
def list_my_articles(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
):
    limit = page_size
    offset = (page - 1) * page_size
    items, total = article_service.list_articles(db, author_id=current_user.id, limit=limit, offset=offset)

    for a in items:
        if a.status == "approved" and a.published_at is None:
            a.published_at = datetime.now(timezone.utc)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


@router.put("/{article_id}/category", response_model=ArticleRead)
def set_article_category(
    article_id: int,
    payload: ArticleCategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:update")),
):
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_owner = article.author_id == current_user.id
    is_admin = _is_reviewer_or_admin(current_user, db)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        return article_relation_service.set_article_category(
            db, article=article, category_id=payload.category_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{article_id}/tags", response_model=ArticleRead)
def set_article_tags(
    article_id: int,
    payload: ArticleTagsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:update")),
):
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_owner = article.author_id == current_user.id
    is_admin = _is_reviewer_or_admin(current_user, db)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        article_relation_service.replace_article_tags(db, article=article, tag_ids=payload.tag_ids)
        return article
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{article_id}/events", response_model=ArticleRead)
def set_article_events(
    article_id: int,
    payload: ArticleEventsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:update")),
):
    article = article_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_owner = article.author_id == current_user.id
    is_admin = _is_reviewer_or_admin(current_user, db)
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        article_relation_service.replace_article_events(db, article=article, event_ids=payload.event_ids)
        return article
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


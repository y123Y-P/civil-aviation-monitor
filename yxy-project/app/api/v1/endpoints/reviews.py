# 文件名:yxy-project/app/api/v1/endpoints/reviews.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\api\v1\endpoints\reviews.py
功能: API接口定义
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.services.rbac_service as rbac_service
import app.services.review_service as review_service

from app.api.deps import get_current_active_user, require_permission
from app.core.database import get_db
from app.schemas.review import (
    PendingArticlePageResponse,
    ReviewActionResponse,
    ReviewHistoryPageResponse,
    ReviewRecordPageResponse,
    ReviewRejectRequest,
)

router = APIRouter(tags=["reviews"])


def _is_reviewer_like(current_user, db: Session) -> bool:
    return (
        current_user.is_superuser
        or rbac_service.user_has_role(db, current_user.id, "reviewer")
        or rbac_service.user_has_role(db, current_user.id, "admin")
    )


@router.post("/submit-draft/{draft_id}", response_model=ReviewActionResponse)
def submit_draft_for_review(
    draft_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:submit_review")),
):
    draft = review_service.get_draft_by_id(db, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft not found")

    is_reviewer = _is_reviewer_like(current_user, db)
    if not is_reviewer and draft.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="not enough permission")

    article = None
    if draft.related_article_id is not None:
        article = review_service.get_article_by_id(db, draft.related_article_id)

    try:
        review_service.submit_draft_for_review(
            db, draft=draft, article=article, submitter_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"ok": True}


@router.post("/submit-article/{article_id}", response_model=ReviewActionResponse)
def submit_article_for_review(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:submit_review")),
):
    article = review_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    is_reviewer = _is_reviewer_like(current_user, db)
    if not is_reviewer and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        review_service.submit_article_for_review(db, article=article, submitter_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"ok": True}


@router.post("/{article_id}/approve", response_model=ReviewActionResponse)
def approve(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("review:approve")),
):
    article = review_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    if not _is_reviewer_like(current_user, db):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        review_service.approve_article(db, article=article, reviewer_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


@router.post("/{article_id}/reject", response_model=ReviewActionResponse)
def reject(
    article_id: int,
    request: ReviewRejectRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("review:reject")),
):
    article = review_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    if not _is_reviewer_like(current_user, db):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        review_service.reject_article(db, article=article, reviewer_id=current_user.id, request=request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


@router.post("/{article_id}/publish", response_model=ReviewActionResponse)
def publish(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:publish")),
):
    article = review_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    if not _is_reviewer_like(current_user, db):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        review_service.publish_article(db, article=article, reviewer_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


@router.post("/{article_id}/offline", response_model=ReviewActionResponse)
def offline(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:offline")),
):
    article = review_service.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="article not found")

    if not _is_reviewer_like(current_user, db):
        raise HTTPException(status_code=403, detail="not enough permission")

    try:
        review_service.offline_article(db, article=article, reviewer_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}


@router.get("/pending", response_model=PendingArticlePageResponse)
def pending_list(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("review:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    keyword: str | None = Query(default=None),
):
    if not _is_reviewer_like(current_user, db):
        raise HTTPException(status_code=403, detail="not enough permission")

    items, total = review_service.list_pending_articles(db, page=page, page_size=page_size, keyword=keyword)
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/article/{article_id}/records", response_model=ReviewRecordPageResponse)
def records_by_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("review:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
):
    if not _is_reviewer_like(current_user, db):
        # 本轮仅 reviewer/admin 可看历史记录
        raise HTTPException(status_code=403, detail="not enough permission")

    items, total = review_service.list_review_records_by_article(
        db, article_id=article_id, page=page, page_size=page_size
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/history", response_model=ReviewHistoryPageResponse)
def history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("review:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    action: str | None = Query(default=None),
    to_status: str | None = Query(default=None),
    reviewer_id: int | None = Query(default=None),
    keyword: str | None = Query(default=None),
):
    if not _is_reviewer_like(current_user, db):
        raise HTTPException(status_code=403, detail="not enough permission")

    items, total = review_service.list_review_history(
        db,
        page=page,
        page_size=page_size,
        action=action,
        to_status=to_status,
        reviewer_id=reviewer_id,
        keyword=keyword,
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_permission, get_current_active_user
from app.core.database import get_db
from app.schemas.draft import (
    DraftCreate,
    DraftPageResponse,
    DraftRead,
    DraftUpdate,
)
import app.services.rbac_service as rbac_service
import app.services.draft_service as draft_service

router = APIRouter(tags=["drafts"])


def _can_view_all(current_user, db: Session, all_requested: bool) -> bool:
    if not all_requested:
        return False
    if current_user.is_superuser:
        return True
    return rbac_service.user_has_role(db, current_user.id, "reviewer") or rbac_service.user_has_role(
        db, current_user.id, "admin"
    )


@router.post("", response_model=DraftRead, status_code=status.HTTP_201_CREATED)
def create_draft(
    payload: DraftCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:create")),
):
    return draft_service.create_draft(db, author_id=current_user.id, data=payload)


@router.get("", response_model=DraftPageResponse)
def list_drafts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:read")),
    all: bool = Query(default=False, description="reviewer/admin 可查看全部草稿"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
):
    show_all = _can_view_all(current_user, db, all_requested=all)
    author_id = None if show_all else current_user.id

    limit = page_size
    offset = (page - 1) * page_size
    items, total = draft_service.list_drafts(db, author_id=author_id, limit=limit, offset=offset)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


@router.get("/{draft_id}", response_model=DraftRead)
def get_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:read")),
):
    draft = draft_service.get_draft_by_id(db, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft not found")

    is_owner = draft.author_id == current_user.id
    is_reviewer = _can_view_all(current_user, db, all_requested=True)
    if not is_owner and not is_reviewer:
        raise HTTPException(status_code=403, detail="not enough permission")

    return draft


@router.put("/{draft_id}", response_model=DraftRead)
def update_draft(
    draft_id: int,
    payload: DraftUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:update")),
):
    draft = draft_service.get_draft_by_id(db, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft not found")

    is_owner = draft.author_id == current_user.id
    is_reviewer = _can_view_all(current_user, db, all_requested=True)
    if not is_owner and not is_reviewer:
        raise HTTPException(status_code=403, detail="not enough permission")

    return draft_service.update_draft(db, draft=draft, data=payload)


@router.delete("/{draft_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("article:delete")),
):
    draft = draft_service.get_draft_by_id(db, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="draft not found")

    is_owner = draft.author_id == current_user.id
    is_reviewer = _can_view_all(current_user, db, all_requested=True)
    if not is_owner and not is_reviewer:
        raise HTTPException(status_code=403, detail="not enough permission")

    draft_service.delete_draft(db, draft=draft)
    return None


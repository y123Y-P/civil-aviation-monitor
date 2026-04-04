from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_optional_current_user, require_permission
from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryListItem, CategoryRead, CategoryUpdate
import app.services.category_service as category_service
import app.services.article_relation_service as article_relation_service
import app.services.rbac_service as rbac_service

router = APIRouter(tags=["categories"])


def _is_admin_like(current_user, db: Session) -> bool:
    if current_user is None:
        return False
    return (
        current_user.is_superuser
        or rbac_service.user_has_role(db, current_user.id, "admin")
        or rbac_service.user_has_role(db, current_user.id, "reviewer")
    )


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("category:manage")),
):
    try:
        return category_service.create_category(db, data=payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def list_categories(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("user:read")),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    keyword: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
):
    items, total = category_service.list_categories(
        db, page=page, page_size=page_size, keyword=keyword, is_active=is_active
    )
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("user:read")),
):
    category = category_service.get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="category not found")
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("category:manage")),
):
    category = category_service.get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="category not found")
    try:
        return category_service.update_category(db, category=category, data=payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    _: object = Depends(require_permission("category:manage")),
):
    category = category_service.get_category_by_id(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="category not found")
    category_service.delete_category(db, category=category)
    return None


@router.get("/{category_id}/articles")
def list_category_articles(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    keyword: str | None = Query(default=None),
):
    if not category_service.get_category_by_id(db, category_id):
        raise HTTPException(status_code=404, detail="category not found")

    is_admin = _is_admin_like(current_user, db)
    items, total = article_relation_service.list_articles_by_category(
        db,
        category_id=category_id,
        current_user_id=current_user.id if current_user is not None else None,
        is_admin=is_admin,
        page=page,
        page_size=page_size,
        keyword=keyword,
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


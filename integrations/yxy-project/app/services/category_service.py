from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug import slugify


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    stmt = select(Category).where(Category.id == category_id)
    return db.execute(stmt).scalars().first()


def list_categories(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 10,
    keyword: str | None = None,
    is_active: bool | None = None,
) -> tuple[list[Category], int]:
    offset = (page - 1) * page_size
    stmt = select(Category).order_by(Category.sort_order.asc(), Category.id.desc())
    count_stmt = select(Category.id)

    filters = []
    if keyword:
        kw = f"%{keyword.strip()}%"
        filters.append(Category.name.like(kw))
    if is_active is not None:
        filters.append(Category.is_active == is_active)

    if filters:
        stmt = stmt.where(*filters)
        count_stmt = count_stmt.where(*filters)

    total = db.execute(count_stmt).all()
    total_count = len(total)
    items = list(db.execute(stmt.limit(page_size).offset(offset)).scalars().all())
    return items, total_count


def create_category(db: Session, *, data: CategoryCreate) -> Category:
    base_slug = data.slug or slugify(data.name)
    # slug 冲突时追加后缀
    slug = base_slug
    idx = 1
    while db.execute(select(Category.id).where(Category.slug == slug)).first() is not None:
        idx += 1
        slug = f"{base_slug}-{idx}"

    category = Category(
        name=data.name,
        slug=slug,
        description=data.description,
        sort_order=data.sort_order,
        is_active=data.is_active,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, *, category: Category, data: CategoryUpdate) -> Category:
    payload = data.model_dump(exclude_none=True)
    if "name" in payload:
        category.name = payload["name"]
    if "slug" in payload and payload["slug"]:
        category.slug = payload["slug"]
    if "description" in payload:
        category.description = payload["description"]
    if "sort_order" in payload:
        category.sort_order = payload["sort_order"]
    if "is_active" in payload:
        category.is_active = payload["is_active"]

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, *, category: Category) -> None:
    db.delete(category)
    db.commit()


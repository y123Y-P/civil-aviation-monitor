from __future__ import annotations

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Article(BaseModel):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)

    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft", index=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 主分类，可为空；用于后续事件专题与聚合查询
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )

    source_type: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    source_url: Mapped[str | None] = mapped_column(String(800), nullable=True)

    published_at: Mapped[str | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status in ('draft','pending_review','approved','rejected','published','offline')",
            name="ck_articles_status",
        ),
        CheckConstraint(
            "source_type in ('manual','generated')",
            name="ck_articles_source_type",
        ),
    )



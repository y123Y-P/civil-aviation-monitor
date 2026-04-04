from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ArticleDraft(BaseModel):
    __tablename__ = "article_drafts"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 草稿如果来自对已有文章的修改，可以关联
    related_article_id: Mapped[int | None] = mapped_column(
        ForeignKey("articles.id", ondelete="SET NULL"), nullable=True, index=True
    )

    source_type: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    source_url: Mapped[str | None] = mapped_column(String(800), nullable=True)

    __table_args__ = (
        CheckConstraint("source_type in ('manual','generated')", name="ck_article_drafts_source_type"),
    )


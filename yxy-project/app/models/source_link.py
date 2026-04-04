from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, CheckConstraint, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SourceLink(BaseModel):
    __tablename__ = "source_links"

    # 注意：url 做 unique 索引时，MySQL + utf8mb4 下索引键长度受限。
    # 若使用过大的 VARCHAR（例如 800），会在迁移创建 unique index 时触发：
    #   1071 Specified key was too long; max key length is 1000 bytes
    # 因此将长度收敛到 200，确保 unique 索引可落库。
    url: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(300), nullable=True)

    raw_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    fetch_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    fetched_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        CheckConstraint("fetch_status in ('pending','success','failed')", name="ck_source_links_fetch_status"),
        Index("ix_source_links_domain_fetch_status", "domain", "fetch_status"),
    )


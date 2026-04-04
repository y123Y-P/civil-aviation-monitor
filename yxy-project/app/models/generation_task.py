from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, String, Text, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class GenerationTask(BaseModel):
    __tablename__ = "generation_tasks"

    source_link_id: Mapped[int] = mapped_column(
        ForeignKey("source_links.id", ondelete="CASCADE"), nullable=False, index=True
    )

    event_title_hint: Mapped[str | None] = mapped_column(String(200), nullable=True)
    keywords_hint: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    summary_hint: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    task_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", index=True
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "task_status in ('pending','processing','completed','failed')",
            name="ck_generation_tasks_status",
        ),
        Index("ix_generation_tasks_status_created_at", "task_status", "created_at"),
    )


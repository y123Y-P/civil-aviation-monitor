# 文件名:integrations/yxy-project/app/models/event.py
# 功能:数据模型与结构定义
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Event(BaseModel):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)

    source_url: Mapped[str | None] = mapped_column(String(800), nullable=True)

    happened_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        CheckConstraint("status in ('active','archived')", name="ck_events_status"),
    )


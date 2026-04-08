# 文件名:integrations/yxy-project/app/models/review_record.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\models\review_record.py
功能: 数据模型定义
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ReviewRecord(BaseModel):
    __tablename__ = "review_records"

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    draft_id: Mapped[int | None] = mapped_column(
        ForeignKey("article_drafts.id", ondelete="SET NULL"), nullable=True, index=True
    )

    reviewer_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    action: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  # submit/approve/reject/publish/offline
    from_status: Mapped[str] = mapped_column(String(30), nullable=False)
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 索引：常用查询维度（轻量）
    __table_args__ = (
        Index("ix_review_records_article_action_created_at", "article_id", "action", "created_at"),
    )


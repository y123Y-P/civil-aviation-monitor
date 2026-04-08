# 文件名:integrations/yxy-project/app/models/article_event.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\models\article_event.py
功能: 数据模型定义
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ArticleEvent(BaseModel):
    __tablename__ = "article_events"

    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )

    __table_args__ = (
        UniqueConstraint("article_id", "event_id", name="uq_article_events_article_id_event_id"),
    )


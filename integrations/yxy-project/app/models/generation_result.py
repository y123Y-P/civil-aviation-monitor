# 文件名:integrations/yxy-project/app/models/generation_result.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\models\generation_result.py
功能: 数据模型定义
"""
from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class GenerationResult(BaseModel):
    __tablename__ = "generation_results"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("generation_tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )

    perspective_code: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    perspective_name: Mapped[str] = mapped_column(String(80), nullable=False)

    title: Mapped[str] = mapped_column(String(220), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(600), nullable=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)
    framework_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # keywords 存 JSON 字符串（本轮简化）
    keywords_json: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    result_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="generated", index=True
    )

    related_draft_id: Mapped[int | None] = mapped_column(
        ForeignKey("article_drafts.id", ondelete="SET NULL"), nullable=True, index=True
    )

    __table_args__ = (
        CheckConstraint(
            "result_status in ('generated','selected','converted','discarded')",
            name="ck_generation_results_status",
        ),
        Index("ix_generation_results_task_perspective", "task_id", "perspective_code"),
    )


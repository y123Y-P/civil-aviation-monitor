# 文件名:integrations/yxy-project/app/schemas/review.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\schemas\review.py
功能: 数据模式定义
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .common import PageResponse


class ReviewRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    article_id: int
    draft_id: Optional[int] = None
    reviewer_id: Optional[int] = None
    action: str
    from_status: str
    to_status: str
    comment: Optional[str] = None
    created_at: datetime


class ReviewRecordListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    article_id: int
    draft_id: Optional[int] = None
    reviewer_id: Optional[int] = None
    action: str
    from_status: str
    to_status: str
    comment: Optional[str] = None
    created_at: datetime


class ReviewRejectRequest(BaseModel):
    comment: Optional[str] = None


class ReviewActionResponse(BaseModel):
    ok: bool = True


class PendingArticleListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    status: str
    author_id: int
    created_at: datetime
    updated_at: datetime


class PendingArticlePageResponse(PageResponse[PendingArticleListItem]):
    pass


class ReviewRecordPageResponse(PageResponse[ReviewRecordListItem]):
    pass


class ReviewHistoryPageResponse(PageResponse[ReviewRecordListItem]):
    pass


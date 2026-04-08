# 文件名:integrations/yxy-project/app/schemas/draft.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\schemas\draft.py
功能: 数据模式定义
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

from .common import PageResponse


class DraftBase(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    content: str

    source_type: str = "manual"
    source_url: Optional[str] = None


class DraftCreate(DraftBase):
    pass


class DraftUpdate(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    content: Optional[str] = None
    source_type: Optional[str] = None
    source_url: Optional[str] = None


class DraftRead(DraftBase):
    id: int
    author_id: int
    related_article_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class DraftListItem(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    author_id: int
    related_article_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class DraftPageResponse(PageResponse[DraftListItem]):
    pass


# 文件名:integrations/yxy-project/app/schemas/article.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\schemas\article.py
功能: 数据模式定义
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

from .common import PageResponse


class ArticleBase(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    content: str

    category_id: Optional[int] = None

    status: str = "draft"
    source_type: str = "manual"
    source_url: Optional[str] = None


class ArticleCreate(ArticleBase):
    # title/内容等仍为必填；status 默认为 draft
    pass


class ArticleUpdate(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    content: Optional[str] = None

    status: Optional[str] = None
    source_type: Optional[str] = None
    source_url: Optional[str] = None


class ArticleRead(ArticleBase):
    id: int
    slug: str
    author_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ArticleListItem(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    status: str
    author_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ArticlePageResponse(PageResponse[ArticleListItem]):
    pass


class ArticleCategoryUpdate(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int | None


class ArticleTagsUpdate(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag_ids: list[int]


class ArticleEventsUpdate(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_ids: list[int]


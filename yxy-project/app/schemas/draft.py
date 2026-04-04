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


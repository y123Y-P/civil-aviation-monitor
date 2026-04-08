# 文件名:yxy-project/app/schemas/tag.py
# 功能:数据模型与结构定义
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    slug: Optional[str] = None
    description: Optional[str] = None


class TagUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TagListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


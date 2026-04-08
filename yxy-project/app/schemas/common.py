# 文件名:yxy-project/app/schemas/common.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\schemas\common.py
功能: 数据模式定义
"""
from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class PageParams(BaseModel):
    page: int = 1
    page_size: int = 10


class PageResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: list[T]


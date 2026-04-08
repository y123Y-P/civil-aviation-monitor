# 文件名:integrations/yxy-project/app/schemas/generation.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\schemas\generation.py
功能: 数据模式定义
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel as PydanticBaseModel, ConfigDict

from .common import PageResponse


class SourceLinkRead(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    domain: str
    title: Optional[str] = None
    fetch_status: str
    extracted_text: Optional[str] = None
    fetched_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime


class GenerationTaskCreate(PydanticBaseModel):
    source_url: str
    event_title_hint: Optional[str] = None
    keywords_hint: Optional[str] = None
    summary_hint: Optional[str] = None


class GenerationTaskRead(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_link_id: int
    event_title_hint: Optional[str] = None
    keywords_hint: Optional[str] = None
    summary_hint: Optional[str] = None
    task_status: str
    created_by: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class GenerationTaskListItem(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_link_id: int
    task_status: str
    created_by: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime


class GenerationResultRead(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    perspective_code: str
    perspective_name: str
    title: str
    summary: Optional[str] = None
    content: str
    framework_note: Optional[str] = None
    keywords_json: Optional[str] = None
    result_status: str
    related_draft_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class GenerationResultListItem(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    perspective_code: str
    perspective_name: str
    title: str
    summary: Optional[str] = None
    result_status: str
    related_draft_id: Optional[int] = None
    created_at: datetime


class ConvertGenerationResultResponse(PydanticBaseModel):
    ok: bool = True
    draft_id: int


class EventAnalysisSchema(PydanticBaseModel):
    event_title: str
    core_facts: list[str]
    entities: list[str]
    keywords: list[str]


class PerspectivePlanSchema(PydanticBaseModel):
    perspectives: list[dict[str, Any]]


class GenerationTaskPageResponse(PageResponse[GenerationTaskListItem]):
    pass


class GenerationResultPageResponse(PageResponse[GenerationResultListItem]):
    pass


class GenerationTaskCreateResponse(PydanticBaseModel):
    ok: bool = True
    task: GenerationTaskRead
    source_link: SourceLinkRead
    results: list[GenerationResultListItem]


class GenerationTaskDetailResponse(PydanticBaseModel):
    ok: bool = True
    task: GenerationTaskRead
    source_link: SourceLinkRead
    results: list[GenerationResultRead]


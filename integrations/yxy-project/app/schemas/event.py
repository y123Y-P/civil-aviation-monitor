from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    status: str = "active"  # active / archived
    source_url: Optional[str] = None
    happened_at: Optional[datetime] = None


class EventUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    source_url: Optional[str] = None
    happened_at: Optional[datetime] = None


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    description: Optional[str] = None
    status: str
    source_url: Optional[str] = None
    happened_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime


class EventListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    status: str
    source_url: Optional[str] = None
    happened_at: Optional[datetime] = None
    created_by: int
    created_at: datetime
    updated_at: datetime


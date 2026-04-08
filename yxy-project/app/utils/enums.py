# 文件名:yxy-project/app/utils/enums.py
# 功能:通用工具函数与辅助逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\utils\enums.py
功能: 工具函数
"""
from __future__ import annotations


ARTICLE_STATUSES: list[str] = [
    "draft",
    "pending_review",
    "approved",
    "rejected",
    "published",
    "offline",
]

SOURCE_TYPES: list[str] = [
    "manual",
    "generated",
]

EVENT_STATUSES: list[str] = [
    "active",
    "archived",
]

# generation module enums
FETCH_STATUSES: list[str] = [
    "pending",
    "success",
    "failed",
]

TASK_STATUSES: list[str] = [
    "pending",
    "processing",
    "completed",
    "failed",
]

GENERATION_RESULT_STATUSES: list[str] = [
    "generated",
    "selected",
    "converted",
    "discarded",
]

PERSPECTIVE_CODES: list[str] = [
    "facts",
    "background",
    "impact",
    "controversy",
    "industry",
    "public_perception",
]


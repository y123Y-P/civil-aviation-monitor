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


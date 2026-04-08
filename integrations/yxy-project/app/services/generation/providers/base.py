# 文件名:integrations/yxy-project/app/services/generation/providers/base.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\generation\providers\base.py
功能: 业务逻辑处理、基础类定义
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PerspectiveDraft:
    title: str
    summary: Optional[str]
    content: str
    framework_note: Optional[str]
    keywords: list[str]


class DraftProvider:
    """
    可插拔草稿生成 provider。

    默认实现使用 rule-based/mock，后续只需要替换 provider 即可接入真实 LLM。
    """

    def generate_for_perspective(
        self,
        *,
        event_title: str,
        core_facts: list[str],
        entities: list[str],
        perspective_code: str,
        perspective_name: str,
        framework_note: str | None,
        keywords: list[str],
        summary_hint: str | None = None,
    ) -> PerspectiveDraft:
        raise NotImplementedError


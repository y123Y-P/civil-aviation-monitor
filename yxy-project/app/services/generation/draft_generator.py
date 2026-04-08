# 文件名:yxy-project/app/services/generation/draft_generator.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\services\generation\draft_generator.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from typing import Protocol

from app.services.generation.event_analyzer import EventAnalysis
from app.services.generation.providers.base import DraftProvider, PerspectiveDraft
from app.services.generation.perspective_planner import PerspectivePlan


class DraftGenerator:
    def __init__(self, *, provider: DraftProvider):
        self.provider = provider

    def generate(
        self,
        *,
        analysis: EventAnalysis,
        plan: PerspectivePlan,
        summary_hint: str | None = None,
    ) -> list[PerspectiveDraft]:
        results: list[PerspectiveDraft] = []
        for p in plan.perspectives:
            draft = self.provider.generate_for_perspective(
                event_title=analysis.event_title,
                core_facts=analysis.core_facts,
                entities=analysis.entities,
                perspective_code=p["perspective_code"],
                perspective_name=p["perspective_name"],
                framework_note=p.get("framework_note"),
                keywords=analysis.keywords,
                summary_hint=summary_hint,
            )
            results.append(draft)
        return results


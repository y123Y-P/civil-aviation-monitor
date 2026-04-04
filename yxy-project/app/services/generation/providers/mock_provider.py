from __future__ import annotations

from typing import Optional

from .base import DraftProvider, PerspectiveDraft


class MockDraftProvider(DraftProvider):
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
        # 规则模板：尽量“围绕同一事件，不伪造事实”，只改变组织方式
        facts_block = "；".join(core_facts[:5])
        entities_block = "、".join(entities[:8]) if entities else "（关键实体待补充）"
        kw_block = ", ".join(keywords[:8]) if keywords else ""

        title = f"{event_title}：{perspective_name}"

        summary = summary_hint or f"从“{perspective_name}”角度梳理事件要点与影响路径。"

        content = (
            f"{title}\n\n"
            f"【核心事实】{facts_block}\n\n"
            f"【关键实体】{entities_block}\n\n"
            f"【{perspective_name}框架】\n"
            f"- 关注焦点：{framework_note or perspective_name}\n"
            f"- 可能的理解路径：结合关键词 {kw_block}\n"
            f"- 结论倾向：基于已知信息的结构化解读（不引入未经证实的新事实）\n\n"
            f"【延展建议】\n"
            f"可进一步补充：原始来源、时间线证据、各方表述差异，以提高解释可靠性。"
        )

        return PerspectiveDraft(
            title=title,
            summary=summary,
            content=content,
            framework_note=framework_note,
            keywords=keywords,
        )


# 文件名:integrations/yxy-project/app/services/generation/perspective_planner.py
# 功能:测试用例与校验逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\generation\perspective_planner.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PerspectivePlan:
    perspectives: list[dict]


class PerspectivePlanner:
    def plan(self, *, event_title: str) -> PerspectivePlan:
        # 固定输出视角（便于前端稳定展示和结果可比）
        perspectives = [
            {"perspective_code": "facts", "perspective_name": "事实梳理", "framework_note": "按时间/因果梳理已知事实，减少解释性假设。"},
            {"perspective_code": "background", "perspective_name": "背景分析", "framework_note": "解释事件发生的背景、环境与上下文。"},
            {"perspective_code": "impact", "perspective_name": "影响评估", "framework_note": "讨论对关键对象的影响与后果路径。"},
            {"perspective_code": "controversy", "perspective_name": "争议讨论", "framework_note": "列出可能的分歧焦点，避免绝对化结论。"},
            {"perspective_code": "industry", "perspective_name": "行业观察", "framework_note": "从行业结构/趋势的角度解读变化与信号。"},
            {"perspective_code": "public_perception", "perspective_name": "公众认知", "framework_note": "讨论公众可能如何理解该事件，以及认知偏差来源。"},
        ]
        return PerspectivePlan(perspectives=perspectives)


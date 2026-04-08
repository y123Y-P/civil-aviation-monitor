# 文件名:integrations/yxy-project/app/services/article_workflow_service.py
# 功能:业务逻辑实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\services\article_workflow_service.py
功能: 业务逻辑处理
"""
from __future__ import annotations

from dataclasses import dataclass


class WorkflowError(ValueError):
    pass


@dataclass(frozen=True)
class Transition:
    action: str
    from_status: list[str]
    to_status: str


TRANSITIONS: dict[str, Transition] = {
    # 提交审核：draft/rejected/offline -> pending_review
    "submit": Transition(action="submit", from_status=["draft", "rejected", "offline"], to_status="pending_review"),
    # 审核
    "approve": Transition(action="approve", from_status=["pending_review"], to_status="approved"),
    "reject": Transition(action="reject", from_status=["pending_review"], to_status="rejected"),
    # 发布/下架
    "publish": Transition(action="publish", from_status=["approved"], to_status="published"),
    "offline": Transition(action="offline", from_status=["published"], to_status="offline"),
}


def validate_transition(current_status: str, *, action: str) -> str:
    """
    集中式状态机校验：
    - 给定当前文章状态 current_status 与动作 action
    - 返回目标状态 to_status
    """

    if action not in TRANSITIONS:
        raise WorkflowError(f"unknown action: {action}")

    transition = TRANSITIONS[action]
    if current_status not in transition.from_status:
        raise WorkflowError(
            f"invalid transition: action={action}, from={current_status}, to={transition.to_status}"
        )

    return transition.to_status


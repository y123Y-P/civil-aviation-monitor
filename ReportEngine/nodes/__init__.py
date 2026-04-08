# 文件名:ReportEngine/nodes/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\ReportEngine\nodes\__init__.py
功能: 处理节点、模块初始化
"""
"""
Report Engine节点处理模块。

封装模板选择、章节生成、文档布局、篇幅规划等流水线节点。
"""

from .base_node import BaseNode, StateMutationNode
from .template_selection_node import TemplateSelectionNode
from .chapter_generation_node import (
    ChapterGenerationNode,
    ChapterJsonParseError,
    ChapterContentError,
    ChapterValidationError,
)
from .document_layout_node import DocumentLayoutNode
from .word_budget_node import WordBudgetNode

__all__ = [
    "BaseNode",
    "StateMutationNode",
    "TemplateSelectionNode",
    "ChapterGenerationNode",
    "ChapterJsonParseError",
    "ChapterContentError",
    "ChapterValidationError",
    "DocumentLayoutNode",
    "WordBudgetNode",
]

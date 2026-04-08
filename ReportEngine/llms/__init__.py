# 文件名:ReportEngine/llms/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\ReportEngine\llms\__init__.py
功能: 大语言模型相关、模块初始化
"""
"""
Report Engine LLM子模块。

目前主要暴露 OpenAI 兼容的 `LLMClient` 封装。
"""

from .base import LLMClient

__all__ = ["LLMClient"]

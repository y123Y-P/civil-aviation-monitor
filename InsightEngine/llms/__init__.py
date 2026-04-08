# 文件名:InsightEngine/llms/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\InsightEngine\llms\__init__.py
功能: 大语言模型相关、模块初始化
"""
"""
LLM module
Provides a unified OpenAI-compatible client for the Insight Engine.
"""

from .base import LLMClient

__all__ = ["LLMClient"]

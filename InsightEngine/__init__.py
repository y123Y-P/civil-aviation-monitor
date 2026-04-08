# 文件名:InsightEngine/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\InsightEngine\__init__.py
功能: 模块初始化
"""
"""
Deep Search Agent
一个无框架的深度搜索AI代理实现
"""

from .agent import DeepSearchAgent, create_agent
from .utils.config import settings, Settings

__version__ = "1.0.0"
__author__ = "Deep Search Agent Team"

__all__ = ["DeepSearchAgent", "create_agent", "settings", "Settings"]

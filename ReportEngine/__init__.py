# 文件名:ReportEngine/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\ReportEngine\__init__.py
功能: 模块初始化
"""
"""
Report Engine。

一个智能报告生成AI代理实现，聚合 Query/Media/Insight 三个子引擎的
Markdown 与论坛讨论，最终落地结构化HTML报告。
"""

from .agent import ReportAgent, create_agent

__version__ = "1.0.0"
__author__ = "Report Engine Team"

__all__ = ["ReportAgent", "create_agent"]

# 文件名:ForumEngine/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\ForumEngine\__init__.py
功能: 模块初始化
"""
"""
ForumEngine - 监控和记录三个Engine的SummaryNode和ReportFormattingNode输出
"""

from .monitor import LogMonitor

__all__ = ['LogMonitor']

# 文件名:ReportEngine/state/__init__.py
# 功能:应用入口与初始化流程
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\ReportEngine\state\__init__.py
功能: 模块初始化
"""
"""
Report Engine状态管理模块。

导出 ReportState/ReportMetadata，供Agent与Flask接口共享。
"""

from .state import ReportState, ReportMetadata

__all__ = ["ReportState", "ReportMetadata"]

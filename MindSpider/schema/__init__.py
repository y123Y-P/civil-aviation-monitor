# 文件名:MindSpider/schema/__init__.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\MindSpider\schema\__init__.py
功能: 数据模式定义、模块初始化
"""
from .models_bigdata import Base as BDBase
from .models_sa import Base as SABase

__all__ = ["BDBase", "SABase"]

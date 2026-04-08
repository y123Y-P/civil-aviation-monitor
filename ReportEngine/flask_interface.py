# 文件名:ReportEngine/flask_interface.py
# 功能:flask_interface 相关实现
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\ReportEngine\flask_interface.py
功能: 模块功能实现
"""
"""
向后兼容：Report Engine 的 HTTP 层已迁移至 fastapi_interface.py。

第三方代码若仍从本模块导入，请改用 fastapi_interface。
"""

from .fastapi_interface import initialize_report_engine, report_router

report_bp = report_router

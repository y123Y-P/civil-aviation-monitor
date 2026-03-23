"""
向后兼容：Report Engine 的 HTTP 层已迁移至 fastapi_interface.py。

第三方代码若仍从本模块导入，请改用 fastapi_interface。
"""

from .fastapi_interface import initialize_report_engine, report_router

report_bp = report_router

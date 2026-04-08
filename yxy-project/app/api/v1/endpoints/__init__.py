# 文件名:yxy-project/app/api/v1/endpoints/__init__.py
# 功能:接口路由与请求处理逻辑
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\app\api\v1\endpoints\__init__.py
功能: API接口定义、模块初始化
"""
from .auth import router as auth_router
from .users import router as users_router
from .roles import router as roles_router
from .permissions import router as permissions_router
from .articles import router as articles_router
from .drafts import router as drafts_router
from .categories import router as categories_router
from .tags import router as tags_router
from .events import router as events_router
from .reviews import router as reviews_router
from .generation import router as generation_router

__all__ = [
    "auth_router",
    "users_router",
    "roles_router",
    "permissions_router",
    "articles_router",
    "drafts_router",
    "categories_router",
    "tags_router",
    "events_router",
    "reviews_router",
    "generation_router",
]


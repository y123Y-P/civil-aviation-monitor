from .user import UserBase, UserOut, UserMeOut
from .auth import RegisterIn, LoginIn, TokenOut
from .role import RoleOut, AssignRolesIn
from .permission import PermissionOut
from .common import PageResponse, PageParams
from .category import CategoryCreate, CategoryUpdate, CategoryRead, CategoryListItem
from .tag import TagCreate, TagUpdate, TagRead, TagListItem
from .event import EventCreate, EventUpdate, EventRead, EventListItem
from .article import ArticleCategoryUpdate, ArticleEventsUpdate, ArticleTagsUpdate
from .review import (
    ReviewRecordRead,
    ReviewRecordListItem,
    ReviewRejectRequest,
    ReviewActionResponse,
    PendingArticleListItem,
    PendingArticlePageResponse,
    ReviewRecordPageResponse,
    ReviewHistoryPageResponse,
)

__all__ = [
    "UserBase",
    "UserOut",
    "UserMeOut",
    "RegisterIn",
    "LoginIn",
    "TokenOut",
    "RoleOut",
    "PermissionOut",
    "AssignRolesIn",
    "PageResponse",
    "PageParams",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryRead",
    "CategoryListItem",
    "TagCreate",
    "TagUpdate",
    "TagRead",
    "TagListItem",
    "EventCreate",
    "EventUpdate",
    "EventRead",
    "EventListItem",
    "ArticleCategoryUpdate",
    "ArticleTagsUpdate",
    "ArticleEventsUpdate",
    "ReviewRecordRead",
    "ReviewRecordListItem",
    "ReviewRejectRequest",
    "ReviewActionResponse",
    "PendingArticleListItem",
    "PendingArticlePageResponse",
    "ReviewRecordPageResponse",
    "ReviewHistoryPageResponse",
]

from .generation import (
    SourceLinkRead,
    GenerationTaskCreate,
    GenerationTaskRead,
    GenerationTaskListItem,
    GenerationResultRead,
    GenerationResultListItem,
    ConvertGenerationResultResponse,
    EventAnalysisSchema,
    PerspectivePlanSchema,
    GenerationTaskPageResponse,
    GenerationResultPageResponse,
    GenerationTaskCreateResponse,
    GenerationTaskDetailResponse,
)

# 注：__all__ 继续追加
__all__ += [
    "SourceLinkRead",
    "GenerationTaskCreate",
    "GenerationTaskRead",
    "GenerationTaskListItem",
    "GenerationResultRead",
    "GenerationResultListItem",
    "ConvertGenerationResultResponse",
    "EventAnalysisSchema",
    "PerspectivePlanSchema",
    "GenerationTaskPageResponse",
    "GenerationResultPageResponse",
    "GenerationTaskCreateResponse",
    "GenerationTaskDetailResponse",
]


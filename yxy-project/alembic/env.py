import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.core.database import Base
from app.models.base import BaseModel  # noqa: F401
from app.models.user import User  # noqa: F401 - 确保模型注册到 Base.metadata
from app.models.role import Role  # noqa: F401
from app.models.permission import Permission  # noqa: F401
from app.models.user_role import UserRole  # noqa: F401
from app.models.role_permission import RolePermission  # noqa: F401
from app.models.article import Article  # noqa: F401
from app.models.article_draft import ArticleDraft  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.tag import Tag  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.article_tag import ArticleTag  # noqa: F401
from app.models.article_event import ArticleEvent  # noqa: F401
from app.models.review_record import ReviewRecord  # noqa: F401
from app.models.source_link import SourceLink  # noqa: F401
from app.models.generation_task import GenerationTask  # noqa: F401
from app.models.generation_result import GenerationResult  # noqa: F401

# Alembic Config 对象
config = context.config

# 配置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 设置数据库URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 目标元数据
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """在离线模式下运行迁移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式下运行迁移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# 文件名:integrations/yxy-project/app/models/base.py
# 功能:数据模型与结构定义
"""
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\app\models\base.py
功能: 数据模型定义、基础类定义
"""
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declared_attr
from ..core.database import Base


class TimestampMixin:
    """时间戳混入类"""
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),
        nullable=False
    )


class BaseModel(Base, TimestampMixin):
    """所有模型的基类"""
    
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls) -> str:
        """自动生成表名"""
        return cls.__name__.lower() + 's'
    
    id = Column(Integer, primary_key=True, index=True)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

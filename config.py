from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent
ENV_FILE: Path = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    HOST: str = Field("0.0.0.0", description="服务器主机地址")
    PORT: int = Field(5000, description="服务器端口")
    
    DB_DIALECT: str = Field("mysql", description="数据库类型")
    DB_HOST: str = Field("localhost", description="数据库主机")
    DB_PORT: int = Field(3306, description="数据库端口")
    DB_USER: str = Field("root", description="数据库用户名")
    DB_PASSWORD: str = Field("", description="数据库密码")
    DB_NAME: str = Field("bettafish", description="数据库名称")
    DB_CHARSET: str = Field("utf8mb4", description="数据库字符集")
    
    INSIGHT_ENGINE_API_KEY: Optional[str] = Field(None, description="Insight Engine API密钥")
    INSIGHT_ENGINE_BASE_URL: Optional[str] = Field(None, description="Insight Engine API基础URL")
    INSIGHT_ENGINE_MODEL_NAME: Optional[str] = Field(None, description="Insight Engine模型名称")
    
    MEDIA_ENGINE_API_KEY: Optional[str] = Field(None, description="Media Engine API密钥")
    MEDIA_ENGINE_BASE_URL: Optional[str] = Field(None, description="Media Engine API基础URL")
    MEDIA_ENGINE_MODEL_NAME: Optional[str] = Field(None, description="Media Engine模型名称")
    
    QUERY_ENGINE_API_KEY: Optional[str] = Field(None, description="Query Engine API密钥")
    QUERY_ENGINE_BASE_URL: Optional[str] = Field(None, description="Query Engine API基础URL")
    QUERY_ENGINE_MODEL_NAME: Optional[str] = Field(None, description="Query Engine模型名称")
    
    REPORT_ENGINE_API_KEY: Optional[str] = Field(None, description="Report Engine API密钥")
    REPORT_ENGINE_BASE_URL: Optional[str] = Field(None, description="Report Engine API基础URL")
    REPORT_ENGINE_MODEL_NAME: Optional[str] = Field(None, description="Report Engine模型名称")
    
    MINDSPIDER_API_KEY: Optional[str] = Field(None, description="MindSpider API密钥")
    MINDSPIDER_BASE_URL: Optional[str] = Field(None, description="MindSpider API基础URL")
    MINDSPIDER_MODEL_NAME: Optional[str] = Field(None, description="MindSpider模型名称")
    
    FORUM_HOST_API_KEY: Optional[str] = Field(None, description="论坛主持人API密钥")
    FORUM_HOST_BASE_URL: Optional[str] = Field(None, description="论坛主持人API基础URL")
    FORUM_HOST_MODEL_NAME: Optional[str] = Field(None, description="论坛主持人模型名称")
    
    KEYWORD_OPTIMIZER_API_KEY: Optional[str] = Field(None, description="关键词优化器API密钥")
    KEYWORD_OPTIMIZER_BASE_URL: Optional[str] = Field(None, description="关键词优化器API基础URL")
    KEYWORD_OPTIMIZER_MODEL_NAME: Optional[str] = Field(None, description="关键词优化器模型名称")
    
    TAVILY_API_KEY: Optional[str] = Field(None, description="Tavily API密钥")
    SEARCH_TOOL_TYPE: str = Field("AnspireAPI", description="网络搜索工具类型")
    ANSPIRE_BASE_URL: Optional[str] = Field(None, description="Anspire API基础URL")
    ANSPIRE_API_KEY: Optional[str] = Field(None, description="Anspire API密钥")
    BOCHA_BASE_URL: Optional[str] = Field(None, description="Bocha API基础URL")
    BOCHA_WEB_SEARCH_API_KEY: Optional[str] = Field(None, description="Bocha Web Search API密钥")
    
    GRAPHRAG_ENABLED: bool = Field(False, description="GraphRAG功能开关")
    GRAPHRAG_MAX_QUERIES: int = Field(3, description="GraphRAG查询次数上限")

    class Config:
        env_file = str(ENV_FILE)
        env_prefix = ""
        case_sensitive = False
        extra = "allow"

_settings_instance: Optional[Settings] = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance

def reload_settings() -> Settings:
    global _settings_instance
    _settings_instance = Settings()
    return _settings_instance

settings = get_settings()

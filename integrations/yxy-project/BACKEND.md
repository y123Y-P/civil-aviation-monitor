<!-- 文件名:integrations/yxy-project/BACKEND.md -->
<!-- 功能:BACKEND 相关实现 -->
# 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\BACKEND.md
# 功能: 模块功能实现

# 后端详细文档（FastAPI + MySQL + SQLAlchemy + Alembic）

## 1. 项目概述
该项目是一个“信息投放网站”后端服务，核心能力包含：
1. 用户注册/登录（JWT）
2. RBAC 角色与权限控制
3. 内容管理（文章 `articles` + 草稿 `article_drafts`）
4. 分类/标签/事件管理（并可用于文章关联聚合）
5. 审核流转（`review_records` 追踪状态变更）
6. 多视角生成（基于网页链接的生成任务与结果，最终可转成草稿）

后端技术栈：
- Web：FastAPI
- ORM：SQLAlchemy 2.0
- 数据库：MySQL（使用 `pymysql`）
- 迁移：Alembic
- 密码哈希：bcrypt
- Token：JWT（`python-jose`）

## 2. 运行入口与启动逻辑
入口文件：`app/main.py`

启动时主要做了：
1. 加载 FastAPI 应用、启用 CORS
2. 启动事件 `startup_event()`：
   - 调用 `app.core.database.init_db()` 检查数据库连接
   - 调用 `safe_seed_rbac(db)` 初始化 RBAC 种子（容错：表未迁移时会跳过）
3. 注册 API 路由：`app.api.v1.api.router` 前缀为 `/api/v1`

> 注意：该项目不会在启动时强制 `Base.metadata.create_all()` 建表，仍推荐使用 `alembic upgrade head` 做迁移。

## 3. 配置（环境变量）
配置类：`app/core/config.py`（Pydantic Settings）

关键环境变量（你当前仓库的 `.env` 示例已包含）：
- `DATABASE_URL`：MySQL 连接串
- `JWT_SECRET_KEY`：JWT 密钥（生产必须替换）
- `JWT_ALGORITHM`：默认 `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`：默认 60
- `REDIS_URL`：预留缓存（当前未在核心逻辑中强依赖）
- `SCRAPING_USER_AGENT`：爬虫/抓取预设

## 4. 数据库与迁移
数据库引擎：`app/core/database.py`
- `engine` 使用 `QueuePool`
- `SessionLocal` 用于提供 SQLAlchemy Session
- `get_db()` 是 FastAPI 的依赖生成器

迁移工具：Alembic
- alembic 配置：`alembic.ini`（`script_location = alembic`）
- 迁移元数据：`alembic/env.py` 使用 `Base.metadata`
- `alembic/versions/*`：当前版本脚本会创建所有表与索引

常用命令：
```powershell
.\venv\Scripts\activate
alembic upgrade head
```

## 5. 认证（Auth）模块
JWT 相关：
- 依赖：`app/api/deps.py` 中 `oauth2_scheme = OAuth2PasswordBearer(...)`
- Token 校验：
  - `decode_access_token(token)` 解析 JWT payload
  - payload 中使用 `sub`（subject）字段作为用户名

密码哈希：
- `app/core/security.py` 已使用 **原生 bcrypt** 实现 `get_password_hash` / `verify_password`
- 相比 passlib 的 bcrypt handler，本实现更适配当前环境

### 5.1 登录接口
路径：`POST /api/v1/auth/login`
入参：`app/schemas/auth.LoginIn`
- `username: str`
- `password: str`

返回：`app/schemas/auth.TokenOut`
- `access_token: str`
- `token_type: "bearer"`
- （可选）`user`

错误：
- 账号不存在、密码错误：`401 invalid credentials`
- 用户被禁用：`403 user is disabled`

### 5.2 注册接口（含角色登记）
路径：`POST /api/v1/auth/register`
入参：`app/schemas/auth.RegisterIn`
- `username`
- `email`
- `password`
- `nickname?`
- `avatar?`
- `role_code: str`
  - 普通注册只允许：`normal_user` / `author`
  - `reviewer/admin` 需要后台分配

注册成功后：
1. 创建 `users` 记录（`status=active`，`is_superuser=False`）
2. 调用 `rbac_service.assign_roles_to_user(...)` 绑定 `role_code`

## 6. RBAC（角色/权限）模块
RBAC 相关依赖：`app/api/deps.py`
 - `require_role(role_code)`
 - `require_permission(permission_code)`

直通规则：
- `current_user.is_superuser=True`：路由级直接放行
- 或用户被绑定 `admin` 角色：放行

### 6.1 权限种子（Seed）
种子：`app/seeds/rbac_seed.py`
默认权限 `DEFAULT_PERMISSIONS`（节选）：
- `user:read`
- `article:create/read/update/delete/submit_review/publish/offline`
- `review:read/approve/reject`
- `category:manage`
- `tag:manage`
- `event:manage`
- `generation:create/read/manage`

默认角色 `DEFAULT_ROLES`（节选）：
- `normal_user`：仅浏览（`user:read`、`article:read`）
- `author`：创建/编辑并提交审核自己的内容
- `reviewer`：审核、发布/下架、管理分类/标签/事件、管理生成任务
- `admin`：预留拥有全部权限（实际绑定由 seed 决定）

Seed 由 `safe_seed_rbac(db)` 在应用启动时执行，且表不存在会容错跳过。

### 6.2 角色分配接口
路径：`POST /api/v1/roles/assign`
入参：`app/schemas/role.AssignRolesIn`
- `user_id: int`
- `role_codes: list[str]`
权限要求：`require_role("admin")`

返回：`list[RoleOut]`（用户当前角色）

## 7. API 网关（路由前缀）
主路由：`app/api/v1/api.py`
所有模块均挂在：`/api/v1`

## 8. 模型（Models）与实体关系（概览）
基础实体：
- `users`
- `roles`
- `permissions`
- `user_roles`（用户-角色）
- `role_permissions`（角色-权限）

内容实体：
- `articles`（正式文章）
- `article_drafts`（草稿）
- `categories`（分类）
- `tags`（标签）
- `events`（事件）
- `article_tags`（文章-标签多对多）
- `article_events`（文章-事件多对多）

审核实体：
- `review_records`（追踪每次状态变更）

生成实体：
- `source_links`（输入网页链接抓取与清洗结果）
- `generation_tasks`（一次生成任务）
- `generation_results`（每个视角生成的结果，可转成草稿）

## 9. 文章与草稿状态流转（审核系统）
文章状态（来自 `app/utils/enums.py`）：
- `draft`
- `pending_review`
- `approved`
- `rejected`
- `published`
- `offline`

审核动作写入 `review_records`：
- `action`：submit / approve / reject / publish / offline
- `from_status` / `to_status`：每次流转追踪
- `comment`：驳回/意见

审核接口只允许 reviewer/admin 发起 approve/reject/publish/offline。

## 10. 多视角生成模块
输入：`generation/create` 基于网页链接抓取内容后，进行事件识别、视角规划、多草稿生成。

数据落库：
- `source_links`：url、domain、raw_html、extracted_text、fetch_status
- `generation_tasks`：参数提示（event_title_hint / keywords_hint / summary_hint）与任务状态
- `generation_results`：每个视角生成的 title/summary/content/framework_note/keywords_json

可插拔 DraftProvider 接口：
- `app/services/generation/providers/base.py`：定义 provider 抽象
- `app/services/generation/providers/mock_provider.py`：当前默认模板化/mock 实现

生成子模块：
- `ContentFetcher`：拉取 HTML
- `ContentExtractor`：提取正文文本（BeautifulSoup/lxml）
- `EventAnalyzer`：规则/启发式事件分析（mock）
- `PerspectivePlanner`：固定视角规划（facts/background/impact/controversy/industry/public_perception）
- `DraftGenerator`：按视角调用 provider 生成草稿内容

生成服务入口：`app/services/generation_service.py`

## 11. 详细 API 文档（按模块）
> 以下路径均已包含 `/api/v1` 前缀（例如 `POST /auth/login` 实际为 `/api/v1/auth/login`）。

### 11.1 Auth
1. `POST /auth/register`
   - 注册并绑定角色（role_code）
2. `POST /auth/login`
   - 登录并返回 JWT

### 11.2 Users
1. `GET /users/me`
2. `GET /users/me/permissions`
   - 返回：用户信息 + roles + permissions（前端用于权限控制）

### 11.3 Roles
1. `GET /roles`
   - 权限：`admin`
2. `POST /roles/assign`
   - 分配角色给用户（权限：`admin`）

### 11.4 Permissions
1. `GET /permissions`

### 11.5 Drafts
1. `POST /drafts`（创建草稿）
   - 权限：`article:create`
2. `GET /drafts`（我的/全部草稿）
   - 权限：`article:read`
   - query：`all`（reviewer/admin 可看全部）
3. `GET /drafts/{draft_id}`（草稿详情）
   - 权限：`article:read`
4. `PUT /drafts/{draft_id}`（更新草稿）
   - 权限：`article:update`
5. `DELETE /drafts/{draft_id}`（删除草稿）
   - 权限：`article:delete`

### 11.6 Articles
1. `POST /articles`（创建文章，默认 draft 状态）
   - 权限：`article:create`
2. `GET /articles`（列表，支持过滤/关键词）
   - 权限：`article:read`
3. `GET /articles/{article_id}`（详情）
   - 权限：`article:read`
4. `PUT /articles/{article_id}`（更新）
   - 权限：`article:update`
5. `DELETE /articles/{article_id}`（删除）
   - 权限：`article:delete`
6. `GET /articles/me/list`（我的文章列表）
   - 权限：`article:read`
7. 绑定分类/标签/事件：
   - `PUT /articles/{article_id}/category`（入参：`category_id`）
   - `PUT /articles/{article_id}/tags`（入参：`tag_ids`）
   - `PUT /articles/{article_id}/events`（入参：`event_ids`）
   - 权限：`article:update`

### 11.7 Reviews（审核流转）
1. `POST /reviews/submit-draft/{draft_id}`
   - 草稿提交审核
   - 权限：`article:submit_review`
2. `POST /reviews/submit-article/{article_id}`
   - 直接提交文章审核（例如 rejected/offline 后重提审）
3. `POST /reviews/{article_id}/approve`
   - 权限：`review:approve`
4. `POST /reviews/{article_id}/reject`
   - 权限：`review:reject`
5. `POST /reviews/{article_id}/publish`
   - 权限：`article:publish`
6. `POST /reviews/{article_id}/offline`
   - 权限：`article:offline`

查询：
- `GET /reviews/pending`
  - 权限：`review:read`
- `GET /reviews/article/{article_id}/records`
  - 权限：`review:read`
- `GET /reviews/history`
  - 权限：`review:read`

### 11.8 Categories
1. `POST /categories`（新增）
   - 权限：`category:manage`
2. `GET /categories`（列表）
   - 权限：`user:read`
3. `GET /categories/{category_id}`（详情）
4. `PUT /categories/{category_id}`（更新）
   - 权限：`category:manage`
5. `DELETE /categories/{category_id}`（删除）
   - 权限：`category:manage`
6. `GET /categories/{category_id}/articles`
   - 权限：`article:read`

### 11.9 Tags
1. `POST /tags`
   - 权限：`tag:manage`
2. `GET /tags`
   - 权限：`user:read`
3. `GET /tags/{tag_id}`
4. `PUT /tags/{tag_id}`
   - 权限：`tag:manage`
5. `DELETE /tags/{tag_id}`
   - 权限：`tag:manage`
6. `GET /tags/{tag_id}/articles`
   - 权限：`article:read`

### 11.10 Events
1. `POST /events`
   - 权限：`event:manage`
2. `GET /events`
   - 权限：`user:read`
3. `GET /events/{event_id}`
4. `PUT /events/{event_id}`
   - 权限：`event:manage`
5. `DELETE /events/{event_id}`
   - 权限：`event:manage`
6. `GET /events/{event_id}/articles`
   - 权限：`article:read`

### 11.11 Generation（多视角生成）
1. `POST /generation/tasks`
   - 权限：`generation:create`
   - 同步执行：fetch -> extract -> analyze -> plan -> generate -> store
2. `GET /generation/tasks`
   - 权限：`generation:read`
   - query：`task_status?`
3. `GET /generation/tasks/{task_id}`
   - 权限：`generation:read`
4. `GET /generation/results/{result_id}`
   - 权限：`generation:read`
5. `POST /generation/results/{result_id}/mark-selected`
   - 权限：`generation:manage`
6. `POST /generation/results/{result_id}/convert-to-draft`
   - 权限：`generation:manage`
   - 创建 `article_drafts`，写回 `related_draft_id`

## 12. 关键注意事项
1. **迁移必须成功执行**：数据库表不存在会导致 seed/接口失败。
2. MySQL 的字符串唯一索引长度可能会触发键长度限制（1071），本项目对关键字段做了收敛处理（如 `users.email`、`source_links.url`）。
3. 前端权限展示依赖 `GET /users/me/permissions` 返回的数据。
4. 管理页面需要一个具备 `admin` 权限（或 `is_superuser=1`）的用户。


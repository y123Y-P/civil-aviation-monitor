// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\api\client.ts
// 功能: API接口定义、客户端

import axios, { type AxiosError } from "axios";
import { ElMessage } from "element-plus";

const TOKEN_KEY = "yxy_access_token";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 30000,
});

export { api };

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers = config.headers || {};
    // 后端使用 OAuth2PasswordBearer，token 以 Bearer 传递
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (resp) => resp,
  (err: AxiosError<any>) => {
    if (err.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      // 保持简单：直接跳转登录页，由路由守卫接管
      window.location.href = "/login";
      return Promise.reject(err);
    }
    const msg =
      (err.response?.data && (err.response.data.detail || err.response.data.message)) ||
      err.message ||
      "请求失败";
    // 避免在页面重复弹窗：有需要的页面可自行不显示
    if (typeof msg === "string") ElMessage.error(msg);
    return Promise.reject(err);
  }
);

export interface ApiPageResponse<T> {
  total: number;
  page: number;
  page_size: number;
  items: T[];
}

export interface ApiOk {
  ok: boolean;
}

// ===== Auth =====
export interface LoginIn {
  username: string;
  password: string;
}

export interface RegisterIn {
  username: string;
  email: string;
  password: string;
  nickname?: string | null;
  avatar?: string | null;
  role_code?: string;
}

export interface UserOut {
  id: number;
  username: string;
  email: string;
  nickname?: string | null;
  avatar?: string | null;
  status: string;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface TokenOut {
  access_token: string;
  token_type: string;
  user?: UserOut;
}

export type LoginResponse = TokenOut;

export interface RoleOut {
  id: number;
  name: string;
  code: string;
  description?: string | null;
}

export interface PermissionOut {
  id: number;
  code: string;
  name?: string | null;
}

export interface UserMePermissionsOut {
  id: number;
  username: string;
  email: string;
  nickname?: string | null;
  avatar?: string | null;
  status: string;
  is_superuser: boolean;
  roles: RoleOut[];
  permissions: PermissionOut[] | string[];
}

// 后端 /users/me/permissions 返回 permissions 是 PermissionOut 列表
// 前端 store 里只关心 permission code，因此在 fetchMePermissionsApi 里归一化。
export interface UserMePermissionsResponse {
  user: UserProfile;
  roles: RoleOut[];
  permissions: string[];
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  nickname?: string | null;
  avatar?: string | null;
  status: string;
  is_superuser: boolean;
}

// ===== Review =====
export interface PendingArticleListItem {
  id: number;
  title: string;
  slug: string;
  status: string;
  author_id: number;
  created_at: string;
  updated_at: string;
}

export interface ReviewRejectRequest {
  comment?: string | null;
}

// ===== Generation =====
export interface SourceLinkRead {
  id: number;
  url: string;
  domain: string;
  title?: string | null;
  fetch_status: string;
  extracted_text?: string | null;
  fetched_at?: string | null;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface GenerationTaskCreate {
  source_url: string;
  event_title_hint?: string | null;
  keywords_hint?: string | null;
  summary_hint?: string | null;
}

export interface GenerationTaskRead {
  id: number;
  source_link_id: number;
  event_title_hint?: string | null;
  keywords_hint?: string | null;
  summary_hint?: string | null;
  task_status: string;
  created_by: number;
  error_message?: string | null;
  started_at?: string | null;
  finished_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface GenerationTaskListItem {
  id: number;
  source_link_id: number;
  task_status: string;
  created_by: number;
  error_message?: string | null;
  started_at?: string | null;
  finished_at?: string | null;
  created_at: string;
}

export interface GenerationResultListItem {
  id: number;
  task_id: number;
  perspective_code: string;
  perspective_name: string;
  title: string;
  summary?: string | null;
  result_status: string;
  related_draft_id?: number | null;
  created_at: string;
}

export interface GenerationResultRead extends GenerationResultListItem {
  content: string;
  framework_note?: string | null;
  keywords_json?: string | null;
  updated_at: string;
}

export interface GenerationTaskCreateResponse {
  ok: boolean;
  task: GenerationTaskRead;
  source_link: SourceLinkRead;
  results: GenerationResultListItem[];
}

export interface GenerationTaskDetailResponse {
  ok: boolean;
  task: GenerationTaskRead;
  source_link: SourceLinkRead;
  results: GenerationResultRead[];
}

export interface ConvertGenerationResultResponse extends ApiOk {
  draft_id: number;
}

// ===== API Helpers =====
export async function loginApi(username: string, password: string): Promise<LoginResponse> {
  const { data } = await api.post("/api/v1/auth/login", { username, password } satisfies LoginIn);
  // 后端直接返回 TokenOut（access_token/token_type/user）
  return data;
}

export async function registerApi(payload: RegisterIn): Promise<UserOut> {
  const { data } = await api.post("/api/v1/auth/register", payload);
  return data as UserOut;
}

export async function fetchMePermissionsApi(): Promise<UserMePermissionsResponse> {
  const { data } = await api.get("/api/v1/users/me/permissions");

  const permissionsRaw = data.permissions as PermissionOut[];
  const permissions = (permissionsRaw || [])
    .map((p: any) => (typeof p === "string" ? p : p.code))
    .filter(Boolean);

  const roles = (data.roles || []) as RoleOut[];
  const user: UserProfile = {
    id: data.id,
    username: data.username,
    email: data.email,
    nickname: data.nickname,
    avatar: data.avatar,
    status: data.status,
    is_superuser: Boolean(data.is_superuser),
  };

  return {
    user,
    roles,
    permissions,
  };
}

export async function listPendingReviews(params: { page: number; page_size: number; keyword?: string | null }) {
  const { data } = await api.get("/api/v1/reviews/pending", { params });
  return data as ApiPageResponse<PendingArticleListItem>;
}

export async function approveReview(articleId: number): Promise<ApiOk> {
  const { data } = await api.post(`/api/v1/reviews/${articleId}/approve`);
  return data as ApiOk;
}

export async function rejectReview(articleId: number, request: ReviewRejectRequest): Promise<ApiOk> {
  const { data } = await api.post(`/api/v1/reviews/${articleId}/reject`, request);
  return data as ApiOk;
}

export async function submitDraftForReview(draftId: number): Promise<ApiOk> {
  const { data } = await api.post(`/api/v1/reviews/submit-draft/${draftId}`);
  return data as ApiOk;
}

export async function submitArticleForReview(articleId: number): Promise<ApiOk> {
  const { data } = await api.post(`/api/v1/reviews/submit-article/${articleId}`);
  return data as ApiOk;
}

export async function listGenerationTasks(params: { page: number; page_size: number; task_status?: string | null }) {
  const { data } = await api.get("/api/v1/generation/tasks", { params });
  return data as ApiPageResponse<GenerationTaskListItem>;
}

export async function createGenerationTask(payload: GenerationTaskCreate): Promise<GenerationTaskCreateResponse> {
  const { data } = await api.post("/api/v1/generation/tasks", payload);
  return data as GenerationTaskCreateResponse;
}

export async function getGenerationTaskDetail(taskId: number): Promise<GenerationTaskDetailResponse> {
  const { data } = await api.get(`/api/v1/generation/tasks/${taskId}`);
  return data as GenerationTaskDetailResponse;
}

export async function markGenerationResultSelected(resultId: number): Promise<GenerationResultRead> {
  const { data } = await api.post(`/api/v1/generation/results/${resultId}/mark-selected`);
  return data as GenerationResultRead;
}

export async function convertGenerationResultToDraft(resultId: number): Promise<ConvertGenerationResultResponse> {
  const { data } = await api.post(`/api/v1/generation/results/${resultId}/convert-to-draft`);
  return data as ConvertGenerationResultResponse;
}


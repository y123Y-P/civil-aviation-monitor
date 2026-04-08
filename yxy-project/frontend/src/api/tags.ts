// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\api\tags.ts
// 功能: API接口定义

import { api, type ApiOk, type ApiPageResponse } from "./client";
import type { TagCreate, TagListItem, TagUpdate } from "../types/tag";

export async function listTags(params: { page: number; page_size: number; keyword?: string | null }) {
  const { data } = await api.get("/api/v1/tags", { params });
  return data as ApiPageResponse<TagListItem>;
}

export async function createTag(payload: TagCreate): Promise<TagListItem> {
  const { data } = await api.post("/api/v1/tags", payload);
  return data as TagListItem;
}

export async function updateTag(tagId: number, payload: TagUpdate): Promise<TagListItem> {
  const { data } = await api.put(`/api/v1/tags/${tagId}`, payload);
  return data as TagListItem;
}

export async function deleteTag(tagId: number): Promise<ApiOk> {
  const resp = await api.delete(`/api/v1/tags/${tagId}`);
  return (resp.data ?? { ok: true }) as ApiOk;
}


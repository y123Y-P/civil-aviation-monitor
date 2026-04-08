// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\api\events.ts
// 功能: API接口定义

import { api, type ApiOk, type ApiPageResponse } from "./client";
import type { EventCreate, EventListItem, EventRead, EventUpdate } from "../types/event";
import type { ArticleListItem } from "../types/article";

export async function listEvents(params: { page: number; page_size: number; keyword?: string | null; status?: string | null }) {
  const { data } = await api.get("/api/v1/events", {
    params: {
      page: params.page,
      page_size: params.page_size,
      keyword: params.keyword || null,
      status: params.status || null,
    },
  });
  return data as ApiPageResponse<EventListItem>;
}

export async function getEventDetail(eventId: number): Promise<EventRead> {
  const { data } = await api.get(`/api/v1/events/${eventId}`);
  return data as EventRead;
}

export async function createEvent(payload: EventCreate): Promise<EventRead> {
  const { data } = await api.post("/api/v1/events", payload);
  return data as EventRead;
}

export async function updateEvent(eventId: number, payload: EventUpdate): Promise<EventRead> {
  const { data } = await api.put(`/api/v1/events/${eventId}`, payload);
  return data as EventRead;
}

export async function deleteEvent(eventId: number): Promise<ApiOk> {
  const resp = await api.delete(`/api/v1/events/${eventId}`);
  return (resp.data ?? { ok: true }) as ApiOk;
}

export async function listEventArticles(
  eventId: number,
  params: { page: number; page_size: number }
): Promise<ApiPageResponse<ArticleListItem>> {
  const { data } = await api.get(`/api/v1/events/${eventId}/articles`, {
    params: { page: params.page, page_size: params.page_size },
  });
  return data as ApiPageResponse<ArticleListItem>;
}


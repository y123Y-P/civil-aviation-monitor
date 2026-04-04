import { api, type ApiOk, type ApiPageResponse } from "./client";
import type { DraftListItem, DraftRead, DraftUpdate, DraftCreate } from "../types/draft";

export async function listMyDrafts(params: { page: number; page_size: number; all?: boolean }) {
  const { data } = await api.get("/api/v1/drafts", {
    params: {
      page: params.page,
      page_size: params.page_size,
      all: params.all ?? false,
    },
  });
  return data as ApiPageResponse<DraftListItem>;
}

export async function getDraftDetail(draftId: number): Promise<DraftRead> {
  const { data } = await api.get(`/api/v1/drafts/${draftId}`);
  return data as DraftRead;
}

export async function updateDraftDetail(draftId: number, payload: DraftUpdate): Promise<DraftRead> {
  const { data } = await api.put(`/api/v1/drafts/${draftId}`, payload);
  return data as DraftRead;
}

export async function createDraft(payload: DraftCreate): Promise<DraftRead> {
  const { data } = await api.post(`/api/v1/drafts`, payload);
  return data as DraftRead;
}

export async function deleteDraft(draftId: number): Promise<ApiOk> {
  const resp = await api.delete(`/api/v1/drafts/${draftId}`);
  return (resp.data ?? { ok: true }) as ApiOk;
}


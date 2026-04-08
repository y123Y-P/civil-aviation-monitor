// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\types\event.ts
// 功能: 模块功能实现

export interface EventListItem {
  id: number;
  title: string;
  slug: string;
  summary?: string | null;
  status: string;
  source_url?: string | null;
  happened_at?: string | null;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface EventRead extends EventListItem {
  description?: string | null;
}

export interface EventCreate {
  title: string;
  slug?: string | null;
  summary?: string | null;
  description?: string | null;
  status?: string;
  source_url?: string | null;
  happened_at?: string | null;
}

export interface EventUpdate {
  title?: string | null;
  slug?: string | null;
  summary?: string | null;
  description?: string | null;
  status?: string | null;
  source_url?: string | null;
  happened_at?: string | null;
}


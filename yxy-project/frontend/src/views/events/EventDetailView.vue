<!-- 文件名:yxy-project/frontend/src/views/events/EventDetailView.vue -->
<!-- 功能:控制层处理逻辑 -->
<!--
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\views\events\EventDetailView.vue
功能: 页面视图组件
-->
<template>
  <div v-loading="loading">
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="display: flex; gap: 16px; flex-wrap: wrap; align-items: center; justify-content: space-between">
        <div>
          <div style="font-weight: 700; font-size: 18px; margin-bottom: 8px">{{ event?.title }}</div>
          <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 6px">
            <el-tag :type="event?.status === 'active' ? 'success' : 'info'">{{ event?.status }}</el-tag>
            <div style="color: #666">Slug：{{ event?.slug }}</div>
            <div style="color: #666">发生时间：{{ event?.happened_at || "-" }}</div>
          </div>
          <div style="color: #666; margin-bottom: 6px">摘要：{{ event?.summary || "-" }}</div>
          <div style="color: #666">描述：{{ event?.description || "-" }}</div>
        </div>
        <div style="display: flex; gap: 12px">
          <el-button @click="router.push('/console/events')">返回事件列表</el-button>
          <el-button v-if="auth.hasPermission('event:manage')" type="primary" @click="router.push(`/console/events`)" disabled>
            编辑（占位）
          </el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="never">
      <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 12px; flex-wrap: wrap">
        <div style="font-weight: 700; flex: 1">关联文章</div>
        <el-pagination
          background
          :current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="(p: number) => (page = p) && fetchArticles()"
        />
      </div>

      <el-table :data="articles" border style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="260" />
        <el-table-column prop="status" label="状态" width="140">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="更新时间" min-width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { getEventDetail, listEventArticles } from "../../api/events";
import type { EventRead } from "../../types/event";
import type { ArticleListItem } from "../../types/article";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const loading = ref(false);

const event = ref<EventRead | null>(null);
const articles = ref<ArticleListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);

const eventId = computed(() => Number(route.params.eventId));

function statusTagType(status: string) {
  if (status === "published" || status === "approved") return "success";
  if (status === "rejected" || status === "offline") return "danger";
  if (status === "pending_review") return "warning";
  return "info";
}

async function fetchArticles() {
  const res = await listEventArticles(eventId.value, { page: page.value, page_size: pageSize.value });
  articles.value = res.items || [];
  total.value = res.total || 0;
}

async function fetchDetail() {
  loading.value = true;
  try {
    event.value = await getEventDetail(eventId.value);
    await fetchArticles();
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchDetail();
});
</script>


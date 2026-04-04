<template>
  <div style="padding: 24px; max-width: 1100px; margin: 0 auto">
    <el-button @click="router.back()" style="margin-bottom: 12px">返回</el-button>

    <el-card shadow="never" style="margin-bottom: 16px" v-loading="loading">
      <div style="font-size: 22px; font-weight: 800; margin-bottom: 8px">{{ event?.title || "-" }}</div>
      <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 10px">
        <el-tag :type="event?.status === 'active' ? 'success' : 'info'">{{ event?.status || "-" }}</el-tag>
        <div style="color: #666">Slug：{{ event?.slug }}</div>
        <div style="color: #666">发生时间：{{ event?.happened_at || "-" }}</div>
      </div>
      <div style="color: #666; margin-bottom: 6px">摘要：{{ event?.summary || "-" }}</div>
      <div style="color: #666">{{ event?.description || "-" }}</div>
    </el-card>

    <el-alert
      v-if="!auth.isAuthenticated"
      title="请先登录后查看事件关联文章列表"
      type="warning"
      show-icon
      style="margin-bottom: 16px"
    />

    <el-card shadow="never" v-else>
      <div style="font-weight: 700; margin-bottom: 12px">关联文章</div>
      <el-table :data="articles" border style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="260" />
        <el-table-column prop="status" label="状态" width="140">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="router.push(`/articles/${row.id}`)">详情</el-button>
          </template>
        </el-table-column>
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

const eventId = computed(() => Number(route.params.eventId));

async function fetchDetail() {
  loading.value = true;
  try {
    if (!auth.isAuthenticated) return;
    event.value = await getEventDetail(eventId.value);
    const res = await listEventArticles(eventId.value, { page: 1, page_size: 10 });
    articles.value = res.items || [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => fetchDetail());
</script>


<!-- 文件名:integrations/yxy-project/frontend/src/views/public/PublicArticleDetailView.vue -->
<!-- 功能:控制层处理逻辑 -->
<!--
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\views\public\PublicArticleDetailView.vue
功能: 页面视图组件
-->
<template>
  <div style="padding: 24px; max-width: 1100px; margin: 0 auto">
    <el-button @click="router.back()" style="margin-bottom: 12px">返回</el-button>

    <el-card shadow="never" v-loading="loading">
      <div style="font-size: 22px; font-weight: 800; margin-bottom: 8px">{{ article?.title || "-" }}</div>
      <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 10px">
        <el-tag :type="article?.status === 'published' ? 'success' : 'info'">{{ articleStatusLabel(article?.status) }}</el-tag>
        <div style="color: #666">作者ID：{{ article?.author_id }}</div>
        <div style="color: #666">发布时间：{{ article?.published_at || "-" }}</div>
      </div>
      <div style="color: #666; margin-bottom: 12px">摘要：{{ article?.summary || "-" }}</div>
      <div style="border: 1px solid #f0f0f0; border-radius: 8px; padding: 12px; white-space: pre-wrap; overflow: auto; max-height: 520px">
        {{ article?.content || "-" }}
      </div>
    </el-card>

    <el-alert
      v-if="!auth.isAuthenticated"
      title="请先登录后查看文章详情"
      type="warning"
      show-icon
      style="margin-top: 16px"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { getArticleDetail } from "../../api/articles";
import type { ArticleRead } from "../../types/article";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const loading = ref(false);
const article = ref<ArticleRead | null>(null);

const articleId = computed(() => Number(route.params.articleId));

function articleStatusLabel(status?: string | null) {
  if (status === "draft") return "草稿";
  if (status === "pending_review") return "待审核";
  if (status === "approved") return "已通过";
  if (status === "rejected") return "已驳回";
  if (status === "published") return "已发布";
  if (status === "offline") return "已下线";
  return status || "-";
}

async function fetchDetail() {
  loading.value = true;
  try {
    article.value = await getArticleDetail(articleId.value);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchDetail();
});
</script>


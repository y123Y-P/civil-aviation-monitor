<template>
  <div>
    <div style="display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px">
      <el-card style="flex: 1; min-width: 260px" shadow="never">
        <div style="font-weight: 700; margin-bottom: 8px">当前用户</div>
        <div>用户名：{{ auth.user?.username }}</div>
        <div>邮箱：{{ auth.user?.email }}</div>
        <div>状态：{{ userStatusLabel(auth.user?.status) }}</div>
        <div>权限：{{ auth.permissions.length }} 条</div>
      </el-card>

      <el-card style="flex: 1; min-width: 260px" shadow="never">
        <div style="font-weight: 700; margin-bottom: 8px">基础统计（占位）</div>
        <div>待审核：{{ placeholder.pendingReviews }}</div>
        <div>生成任务：{{ placeholder.generationTasks }}</div>
        <div>我的草稿：{{ placeholder.myDrafts }}</div>
        <div>我的文章：{{ placeholder.myArticles }}</div>
      </el-card>
    </div>

    <el-card shadow="never">
      <div style="font-weight: 700; margin-bottom: 12px">快速入口</div>
      <div style="display: flex; gap: 12px; flex-wrap: wrap">
        <el-button v-if="auth.hasPermission('review:read')" type="primary" @click="go('/console/reviews')">审核管理</el-button>
        <el-button v-if="auth.hasPermission('generation:read')" @click="go('/console/generation/tasks')">生成任务</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const placeholder = reactive({
  pendingReviews: 0,
  generationTasks: 0,
  myDrafts: 0,
  myArticles: 0,
});

function go(path: string) {
  router.push(path);
}

function userStatusLabel(status?: string | null) {
  if (status === "active") return "正常";
  if (status === "inactive") return "停用";
  if (status === "locked") return "锁定";
  return status || "-";
}
</script>


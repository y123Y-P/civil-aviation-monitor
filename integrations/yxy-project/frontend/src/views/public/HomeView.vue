<!-- 文件名:integrations/yxy-project/frontend/src/views/public/HomeView.vue -->
<!-- 功能:控制层处理逻辑 -->
<!--
文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\views\public\HomeView.vue
功能: 页面视图组件
-->
<template>
  <div style="padding: 24px; max-width: 1100px; margin: 0 auto">
    <div style="font-size: 22px; font-weight: 800; margin-bottom: 8px">信息投放网站</div>
    <div style="color: #666; margin-bottom: 18px">公开内容骨架页：文章列表、文章详情、事件专题。</div>

    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="font-weight: 700; margin-bottom: 10px">快速入口</div>
      <div style="display: flex; gap: 12px; flex-wrap: wrap">
        <el-button type="primary" @click="router.push('/articles')">文章列表</el-button>
        <el-button v-if="auth.isAuthenticated" @click="router.push('/events/1')">事件专题（示例）</el-button>
        <el-button v-else @click="router.push('/login')">登录后查看更多</el-button>
      </div>
    </el-card>

    <el-card shadow="never">
      <div style="font-weight: 700; margin-bottom: 10px">说明</div>
      <div style="color: #666; white-space: pre-wrap">
        当前后端的文章/事件查询接口对登录用户做了权限校验（`user:read`）。
        因此在未登录状态下，公开页面只提供结构骨架；登录后可逐步补充真实数据抓取。
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const auth = useAuthStore();
</script>


<template>
  <el-container style="min-height: 100vh">
    <el-aside width="240px" style="background: #2f3b52">
      <div style="padding: 16px 16px 8px; color: #fff; font-weight: 600">YXY 后台管理</div>
      <el-menu
        :default-active="activePath"
        background-color="#2f3b52"
        text-color="#c7d0e0"
        active-text-color="#fff"
        router
      >
        <el-menu-item index="/console">
          <span>控制台</span>
        </el-menu-item>

        <!-- 登录后可快速查看公开文章列表（approved/published） -->
        <el-menu-item v-if="auth.isAuthenticated" index="/articles">
          <span>查看已发布文章</span>
        </el-menu-item>

        <el-menu-item
          v-if="auth.hasPermission('article:read')"
          index="/console/articles"
        >
          <span>我的文章</span>
        </el-menu-item>

        <el-menu-item
          v-if="auth.hasPermission('article:read')"
          index="/console/drafts"
        >
          <span>我的草稿</span>
        </el-menu-item>

        <el-menu-item
          v-if="auth.hasPermission('review:read') || auth.hasPermission('review:approve')"
          index="/console/reviews"
        >
          <span>审核管理</span>
        </el-menu-item>

        <el-menu-item
          v-if="auth.hasPermission('category:manage')"
          index="/console/categories"
        >
          <span>分类管理</span>
        </el-menu-item>

        <el-menu-item
          v-if="auth.hasPermission('tag:manage')"
          index="/console/tags"
        >
          <span>标签管理</span>
        </el-menu-item>

        <el-menu-item
          v-if="auth.hasPermission('event:manage')"
          index="/console/events"
        >
          <span>事件管理</span>
        </el-menu-item>

        <el-menu-item v-if="auth.hasPermission('generation:read') || auth.hasPermission('generation:create')" index="/console/generation/tasks">
          <span>生成任务</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="background: #fff; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f0f0f0">
        <div style="font-weight: 600">当前页面：{{ activeTitle }}</div>
        <div style="display: flex; align-items: center; gap: 12px">
          <div style="color: #666">
            {{ auth.user ? auth.user.username : "" }}
          </div>
          <el-button type="primary" link @click="onLogout">退出</el-button>
        </div>
      </el-header>

      <el-main style="background: #f6f7fb">
        <div style="background: #fff; padding: 16px; border-radius: 8px">
          <router-view />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const activePath = computed(() => (route.path.startsWith("/console") ? route.path : "/console"));

const activeTitle = computed(() => {
  if (activePath.value === "/console") return "控制台首页";
  if (activePath.value === "/console/articles") return "我的文章";
  if (activePath.value === "/console/drafts") return "我的草稿";
  if (activePath.value.startsWith("/console/drafts/")) return "草稿详情";
  if (activePath.value === "/console/reviews") return "审核管理";
  if (activePath.value === "/console/categories") return "分类管理";
  if (activePath.value === "/console/tags") return "标签管理";
  if (activePath.value === "/console/events") return "事件管理";
  if (activePath.value.startsWith("/console/events/")) return "事件详情";
  if (activePath.value === "/console/generation/tasks") return "生成任务";
  if (activePath.value.startsWith("/console/generation/tasks/")) return "生成任务详情";
  return "页面";
});

async function onLogout() {
  auth.logout();
  await router.push("/login");
}
</script>


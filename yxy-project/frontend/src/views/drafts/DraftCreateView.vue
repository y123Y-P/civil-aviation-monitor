<!-- 文件名:yxy-project/frontend/src/views/drafts/DraftCreateView.vue -->
<!-- 功能:控制层处理逻辑 -->
<!--
文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\views\drafts\DraftCreateView.vue
功能: 页面视图组件
-->
<template>
  <div v-loading="loading">
    <el-card shadow="never">
      <div style="font-weight: 700; margin-bottom: 12px">新建草稿</div>

      <el-form :model="form" label-width="100px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="3" placeholder="可选摘要" />
        </el-form-item>
        <el-form-item label="正文" required>
          <el-input v-model="form.content" type="textarea" :rows="10" placeholder="先写点内容（必填）" />
        </el-form-item>
      </el-form>

      <div style="display: flex; gap: 12px; margin-top: 12px; flex-wrap: wrap">
        <el-button type="primary" :disabled="loading" @click="onCreate">
          创建并进入编辑
        </el-button>
        <el-button @click="router.push('/console/drafts')">返回草稿列表</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { createDraft } from "../../api/drafts";
import { useAuthStore } from "../../stores/auth";
import type { DraftCreate as DraftCreatePayload } from "../../types/draft";

const router = useRouter();
const auth = useAuthStore();

const loading = ref(false);

const form = reactive<DraftCreatePayload>({
  title: "",
  summary: null,
  cover_image: null,
  content: "",
  source_type: "manual",
  source_url: null,
});

async function onCreate() {
  if (!form.title.trim()) {
    ElMessage.warning("请输入标题");
    return;
  }
  if (!form.content.trim()) {
    ElMessage.warning("请输入正文（必填）");
    return;
  }

  loading.value = true;
  try {
    const created = await createDraft(form);
    ElMessage.success("草稿创建成功");
    router.push(`/console/drafts/${created.id}`);
  } finally {
    loading.value = false;
  }
}
</script>


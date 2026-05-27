<template>
  <div v-loading="loading">
    <el-card shadow="never">
      <div style="display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; align-items: center">
        <div style="font-weight: 700">编辑文章</div>
        <el-button @click="router.push('/console/articles')">返回</el-button>
      </div>

      <el-form :model="form" label-width="90px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" />
        </el-form-item>

        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="3" />
        </el-form-item>

        <el-form-item label="正文" required>
          <el-input v-model="form.content" type="textarea" :rows="14" />
        </el-form-item>
      </el-form>

      <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px">
        <el-button type="primary" :disabled="saving" @click="onSave">保存</el-button>
        <el-button
          v-if="auth.hasPermission('article:submit_review')"
          type="success"
          :disabled="saving"
          @click="onSubmitForReview"
        >
          提交审核
        </el-button>
        <el-button
          v-if="auth.hasPermission('article:update')"
          type="danger"
          :disabled="saving"
          @click="onDelete"
        >
          删除
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { useAuthStore } from "../../stores/auth";
import { getArticleDetail, updateArticleDetail, deleteArticle } from "../../api/articles";
import { submitArticleForReview } from "../../api/client";
import type { ArticleRead, ArticleUpdate } from "../../types/article";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const loading = ref(false);
const saving = ref(false);

const article = ref<ArticleRead | null>(null);

const form = reactive<ArticleUpdate>({
  title: "",
  summary: null,
  cover_image: null,
  content: "",
  status: null,
  source_type: null,
  source_url: null,
});

const articleId = computed(() => Number(route.params.articleId));

async function fetchDetail() {
  loading.value = true;
  try {
    article.value = await getArticleDetail(articleId.value);
    form.title = article.value.title;
    form.summary = article.value.summary || null;
    form.content = article.value.content;
  } finally {
    loading.value = false;
  }
}

async function onSave() {
  if (!form.title?.trim() || !form.content?.trim()) {
    ElMessage.warning("标题和正文不能为空");
    return;
  }

  saving.value = true;
  try {
    await updateArticleDetail(articleId.value, {
      title: form.title,
      summary: form.summary || null,
      content: form.content,
    });
    ElMessage.success("保存成功");
    await fetchDetail();
  } finally {
    saving.value = false;
  }
}

async function onDelete() {
  try {
    await ElMessageBox.confirm("确认删除该文章？", "删除确认", { type: "warning" });
    saving.value = true;
    await deleteArticle(articleId.value);
    ElMessage.success("删除成功");
    router.push("/console/articles");
  } catch {
    // cancel/error
  } finally {
    saving.value = false;
  }
}

async function onSubmitForReview() {
  if (!form.title?.trim() || !form.content?.trim()) {
    ElMessage.warning("标题和正文不能为空");
    return;
  }

  saving.value = true;
  try {
    await updateArticleDetail(articleId.value, {
      title: form.title,
      summary: form.summary || null,
      content: form.content,
    });
    await submitArticleForReview(articleId.value);
    ElMessage.success("提交审核成功");
    await fetchDetail();
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  fetchDetail();
});
</script>


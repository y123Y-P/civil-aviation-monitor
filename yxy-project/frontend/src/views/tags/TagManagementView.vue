<template>
  <div v-loading="loading">
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap">
        <el-input
          v-model="keyword"
          style="width: 320px"
          placeholder="按名称/slug搜索（可选）"
          clearable
        />
        <el-button type="primary" @click="fetchList">搜索</el-button>
        <div style="flex: 1" />
        <el-button type="primary" :disabled="loading" @click="openCreate">新增标签</el-button>
      </div>
    </el-card>

    <el-table :data="items" border style="width: 100%">
      <el-table-column prop="name" label="名称" min-width="220" />
      <el-table-column prop="slug" label="Slug" min-width="200" />
      <el-table-column prop="description" label="描述" min-width="260">
        <template #default="{ row }">
          <span v-if="row.description">{{ truncate(row.description, 60) }}</span>
          <span v-else style="color: #999">-</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-space>
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="onDelete(row.id)" :loading="deletingId === row.id">
              删除
            </el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top: 12px; display: flex; justify-content: flex-end">
      <el-pagination
        background
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="(p: number) => (page = p) && fetchList()"
      />
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? '新增标签' : '编辑标签'" width="520px" @close="resetForm">
      <el-form :model="form" label-width="100px" :rules="rules">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Slug">
          <el-input v-model="form.slug" placeholder="可选" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="onSubmit">
          {{ dialogMode === "create" ? "创建" : "保存" }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { TagCreate, TagListItem, TagUpdate } from "../../types/tag";
import { listTags, createTag, updateTag, deleteTag } from "../../api/tags";

const loading = ref(false);
const items = ref<TagListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const keyword = ref<string | null>(null);

const deletingId = ref<number | null>(null);

const dialogVisible = ref(false);
const dialogMode = ref<"create" | "edit">("create");
const currentId = ref<number | null>(null);
const submitting = ref(false);

const form = reactive<TagCreate & TagUpdate>({
  name: "",
  slug: null,
  description: null,
});

const rules = {
  name: [{ required: true, message: "请输入标签名称", trigger: "blur" }],
};

function truncate(text: string, len: number) {
  return text.length > len ? text.slice(0, len) + "..." : text;
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await listTags({ page: page.value, page_size: pageSize.value, keyword: keyword.value });
    items.value = res.items || [];
    total.value = res.total || 0;
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  dialogMode.value = "create";
  currentId.value = null;
  form.name = "";
  form.slug = null;
  form.description = null;
  dialogVisible.value = true;
}

function openEdit(row: TagListItem) {
  dialogMode.value = "edit";
  currentId.value = row.id;
  form.name = row.name;
  form.slug = row.slug;
  form.description = row.description ?? null;
  dialogVisible.value = true;
}

function resetForm() {
  dialogVisible.value = false;
}

async function onSubmit() {
  submitting.value = true;
  try {
    if (dialogMode.value === "create") {
      await createTag({
        name: form.name,
        slug: form.slug || null,
        description: form.description || null,
      });
      ElMessage.success("创建成功");
    } else if (currentId.value != null) {
      await updateTag(currentId.value, {
        name: form.name,
        slug: form.slug || null,
        description: form.description || null,
      });
      ElMessage.success("保存成功");
    }
    dialogVisible.value = false;
    await fetchList();
  } finally {
    submitting.value = false;
  }
}

async function onDelete(tagId: number) {
  try {
    await ElMessageBox.confirm("确认删除该标签？", "删除确认", { type: "warning" });
    deletingId.value = tagId;
    await deleteTag(tagId);
    ElMessage.success("删除成功");
    await fetchList();
  } catch {
    // cancel/error
  } finally {
    deletingId.value = null;
  }
}

fetchList();
</script>


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
        <el-button type="primary" :disabled="loading" @click="openCreate">新增分类</el-button>
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
      <el-table-column prop="sort_order" label="排序" width="120" />
      <el-table-column prop="is_active" label="是否启用" width="140">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? "active" : "inactive" }}</el-tag>
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

    <el-dialog v-model="dialogVisible" :title="dialogMode === 'create' ? '新增分类' : '编辑分类'" width="560px" @close="resetForm">
      <el-form :model="form" label-width="100px" :rules="rules">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Slug">
          <el-input v-model="form.slug" placeholder="可选，不填则后端生成/使用默认策略" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
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
import type { CategoryListItem } from "../../types/category";
import type { CategoryCreate, CategoryUpdate } from "../../types/category";
import { listCategories, createCategory, updateCategory, deleteCategory } from "../../api/categories";

const loading = ref(false);
const items = ref<CategoryListItem[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const keyword = ref<string | null>(null);

const deletingId = ref<number | null>(null);

const dialogVisible = ref(false);
const dialogMode = ref<"create" | "edit">("create");
const currentId = ref<number | null>(null);
const submitting = ref(false);

const form = reactive<CategoryCreate & CategoryUpdate>({
  name: "",
  slug: null,
  description: null,
  sort_order: 0,
  is_active: true,
});

const rules = {
  name: [{ required: true, message: "请输入分类名称", trigger: "blur" }],
  sort_order: [{ required: true, message: "请输入排序", trigger: "change" }],
};

function truncate(text: string, len: number) {
  return text.length > len ? text.slice(0, len) + "..." : text;
}

async function fetchList() {
  loading.value = true;
  try {
    const res = await listCategories({ page: page.value, page_size: pageSize.value, keyword: keyword.value });
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
  form.sort_order = 0;
  form.is_active = true;
  dialogVisible.value = true;
}

function openEdit(row: CategoryListItem) {
  dialogMode.value = "edit";
  currentId.value = row.id;
  form.name = row.name;
  form.slug = row.slug;
  form.description = row.description ?? null;
  form.sort_order = row.sort_order;
  form.is_active = row.is_active;
  dialogVisible.value = true;
}

function resetForm() {
  dialogVisible.value = false;
}

async function onSubmit() {
  submitting.value = true;
  try {
    if (dialogMode.value === "create") {
      await createCategory({
        name: form.name,
        slug: form.slug || null,
        description: form.description || null,
        sort_order: Number(form.sort_order ?? 0),
        is_active: Boolean(form.is_active),
      });
      ElMessage.success("创建成功");
    } else if (currentId.value != null) {
      await updateCategory(currentId.value, {
        name: form.name,
        slug: form.slug || null,
        description: form.description || null,
        sort_order: Number(form.sort_order ?? 0),
        is_active: Boolean(form.is_active),
      });
      ElMessage.success("保存成功");
    }
    dialogVisible.value = false;
    await fetchList();
  } finally {
    submitting.value = false;
  }
}

async function onDelete(categoryId: number) {
  try {
    await ElMessageBox.confirm("确认删除该分类？", "删除确认", { type: "warning" });
    deletingId.value = categoryId;
    await deleteCategory(categoryId);
    ElMessage.success("删除成功");
    await fetchList();
  } catch {
    // cancel or error
  } finally {
    deletingId.value = null;
  }
}

fetchList();
</script>


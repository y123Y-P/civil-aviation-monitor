// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\yxy-project\frontend\src\router\index.ts
// 功能: 路由配置

import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { useAuthStore } from "../stores/auth";

import AppLayout from "../components/layout/AppLayout.vue";
import LoginView from "../views/auth/LoginView.vue";
import RegisterView from "../views/auth/RegisterView.vue";
import DashboardView from "../views/dashboard/DashboardView.vue";
import MyArticlesView from "../views/articles/MyArticlesView.vue";
import ArticleCreateView from "../views/articles/ArticleCreateView.vue";
import ArticleEditView from "../views/articles/ArticleEditView.vue";
import DraftListView from "../views/drafts/DraftListView.vue";
import DraftDetailView from "../views/drafts/DraftDetailView.vue";
import DraftCreateView from "../views/drafts/DraftCreateView.vue";
import ReviewManagementView from "../views/reviews/ReviewManagementView.vue";
import GenerationTaskView from "../views/generation/GenerationTaskView.vue";
import GenerationTaskDetailView from "../views/generation/GenerationTaskDetailView.vue";
import CategoryManagementView from "../views/categories/CategoryManagementView.vue";
import TagManagementView from "../views/tags/TagManagementView.vue";
import EventManagementView from "../views/events/EventManagementView.vue";
import EventDetailView from "../views/events/EventDetailView.vue";

import HomeView from "../views/public/HomeView.vue";
import ArticleListView from "../views/public/ArticleListView.vue";
import PublicArticleDetailView from "../views/public/PublicArticleDetailView.vue";
import EventTopicView from "../views/public/EventTopicView.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/articles",
    name: "publicArticles",
    component: ArticleListView,
  },
  {
    path: "/articles/:articleId",
    name: "publicArticleDetail",
    component: PublicArticleDetailView,
    props: true,
  },
  {
    path: "/events/:eventId",
    name: "eventTopic",
    component: EventTopicView,
    props: true,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/console",
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      { path: "", name: "dashboard", component: DashboardView },
      { path: "articles", name: "myArticles", component: MyArticlesView },
      { path: "articles/new", name: "articleCreate", component: ArticleCreateView },
      { path: "articles/:articleId", name: "articleEdit", component: ArticleEditView, props: true },
      { path: "drafts", name: "myDrafts", component: DraftListView },
      { path: "drafts/new", name: "draftNew", component: DraftCreateView },
      { path: "drafts/:draftId", name: "draftDetail", component: DraftDetailView, props: true },
      { path: "reviews", name: "reviews", component: ReviewManagementView },
      { path: "categories", name: "categories", component: CategoryManagementView },
      { path: "tags", name: "tags", component: TagManagementView },
      { path: "events", name: "events", component: EventManagementView },
      { path: "events/:eventId", name: "eventDetail", component: EventDetailView, props: true },
      { path: "generation/tasks", name: "generationTasks", component: GenerationTaskView },
      { path: "generation/tasks/:taskId", name: "generationTaskDetail", component: GenerationTaskDetailView, props: true },
    ],
  },
  { path: "/console/*", redirect: "/console" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  const requiresAuth = Boolean(to.meta.requiresAuth);
  const isLogin = to.name === "login";

  if (requiresAuth) {
    if (!auth.isAuthenticated) {
      await auth.restoreAuth();
    }
    if (!auth.isAuthenticated) {
      return { name: "login" };
    }
  } else if (isLogin) {
    if (auth.isAuthenticated) {
      return { name: "dashboard" };
    }
  }

  return true;
});

export default router;


// 文件名: Users\24704\Desktop\civil-aviation-monitor-main\integrations\yxy-project\frontend\src\stores\auth.ts
// 功能: 状态管理、认证授权

import { defineStore } from "pinia";
import { loginApi, fetchMePermissionsApi, type LoginResponse, type UserMePermissionsResponse } from "../api/client";

export type PermissionCode = string;

export interface Role {
  id: number;
  name: string;
  code: string;
  description?: string | null;
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  nickname?: string | null;
  avatar?: string | null;
  status: string;
  is_superuser: boolean;
}

export interface UserRolePermissionState {
  roles: Role[];
  permissions: PermissionCode[];
}

const TOKEN_KEY = "yxy_access_token";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: "" as string,
    user: null as UserProfile | null,
    roles: [] as Role[],
    permissions: [] as PermissionCode[],
    isAuthenticated: false,
    loading: false,
  }),
  actions: {
    loadToken() {
      const t = localStorage.getItem(TOKEN_KEY);
      this.token = t || "";
      this.isAuthenticated = Boolean(this.token);
    },
    async restoreAuth() {
      if (!this.token) this.loadToken();
      if (!this.token) return;
      if (this.user && this.permissions.length) return;
      await this.fetchCurrentUser();
    },
    async login(username: string, password: string) {
      this.loading = true;
      try {
        const res: LoginResponse = await loginApi(username, password);
        this.token = res.access_token;
        localStorage.setItem(TOKEN_KEY, this.token);

        // 拉取 roles/permissions
        await this.fetchCurrentUser();
      } finally {
        this.loading = false;
      }
    },
    async fetchCurrentUser() {
      if (!this.token) return;
      const data: UserMePermissionsResponse = await fetchMePermissionsApi();
      this.user = data.user;
      this.roles = data.roles;
      this.permissions = data.permissions;
      this.isAuthenticated = true;
    },
    logout() {
      this.token = "";
      this.user = null;
      this.roles = [];
      this.permissions = [];
      this.isAuthenticated = false;
      localStorage.removeItem(TOKEN_KEY);
    },
    hasPermission(code: PermissionCode) {
      if (this.user?.is_superuser) return true;
      return this.permissions.includes(code);
    },
  },
});


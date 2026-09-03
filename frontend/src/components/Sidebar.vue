<template>
  <el-aside width="240px" class="sidebar">
    <div class="logo">
      <div class="logo-icon">🌿</div>
      <div class="logo-text">
        <div class="logo-title">中草药智能识别系统</div>
      </div>
    </div>

    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      background-color="#1f2d3d"
      text-color="#c0c4cc"
      active-text-color="#ffffff"
      router
    >
      <el-menu-item index="/dashboard">
        <el-icon><HomeFilled /></el-icon>
        <span>首页</span>
      </el-menu-item>
      <el-menu-item index="/recognition">
        <el-icon><Camera /></el-icon>
        <span>中草药识别</span>
      </el-menu-item>
      <el-menu-item index="/history">
        <el-icon><Clock /></el-icon>
        <span>历史记录</span>
      </el-menu-item>
      <el-menu-item index="/model">
        <el-icon><DataAnalysis /></el-icon>
        <span>模型信息</span>
      </el-menu-item>
    </el-menu>

    <!-- 底部固定：用户信息 -->
    <div class="sidebar-bottom">
      <div class="user-card">
        <el-avatar :size="34" class="user-avatar">
          <el-icon><User /></el-icon>
        </el-avatar>
        <div class="user-info">
          <div class="user-name">{{ username }}</div>
          <div class="user-status">已登录</div>
        </div>
        <el-icon class="logout-btn" title="退出登录" @click="handleLogout">
          <SwitchButton />
        </el-icon>
      </div>
    </div>
  </el-aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { HomeFilled, Camera, Clock, DataAnalysis, User, SwitchButton } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => route.path)
const username = computed(() => localStorage.getItem('herb_user') || 'admin')

const handleLogout = () => {
  localStorage.removeItem('herb_token')
  localStorage.removeItem('herb_user')
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  background: #1f2d3d;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 18px;
  gap: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}
.logo-icon {
  font-size: 24px;
  line-height: 1;
}
.logo-title {
  color: #fff;
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
}
.sidebar-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
}
.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #409eff !important;
}

/* 底部固定区域 */
.sidebar-bottom {
  margin-top: auto;
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-shrink: 0;
}

/* 用户信息卡片 */
.user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 10px;
}
.user-avatar {
  background: #409eff;
  flex-shrink: 0;
}
.user-info {
  flex: 1;
  min-width: 0;
}
.user-name {
  color: #fff;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-status {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 12px;
  margin-top: 2px;
}
.logout-btn {
  color: #909399;
  cursor: pointer;
  font-size: 16px;
}
.logout-btn:hover {
  color: #f56c6c;
}
</style>

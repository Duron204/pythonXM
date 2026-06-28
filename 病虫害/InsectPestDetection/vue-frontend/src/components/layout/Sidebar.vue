<script setup lang="ts">
import { ref } from 'vue'
import { useDetectionStore } from '@/stores/detection'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const emit = defineEmits<{
  (e: 'select-mode', mode: string): void
}>()

const store = useDetectionStore()
const userStore = useUserStore()
const router = useRouter()
const isExpanded = ref(false)

const menuItems = [
  { id: 'image', icon: 'Picture', label: '选择图片', status: '支持JPG/PNG' },
  { id: 'folder', icon: 'FolderOpened', label: '选择文件夹', status: '批量检测' },
  { id: 'camera', icon: 'VideoCamera', label: '开启摄像头', status: '摄像头未开启' },
  { id: 'video', icon: 'VideoPlay', label: '选择视频', status: '支持MP4/AVI' },
  { id: 'model', icon: 'Cpu', label: '选择模型', status: '默认模型' },
]

function toggleSidebar() {
  isExpanded.value = !isExpanded.value
}

function handleSelect(mode: string) {
  emit('select-mode', mode)
}

function goLogin() {
  router.push('/login')
}
</script>

<template>
  <aside class="sidebar" :class="{ expanded: isExpanded }">
    <div class="sidebar-header">
      <button class="menu-btn" @click="toggleSidebar" title="菜单">
        <el-icon :size="20"><Operation /></el-icon>
      </button>
    </div>

    <nav class="sidebar-nav">
      <div
        v-for="item in menuItems"
        :key="item.id"
        class="nav-item"
        :class="{ active: store.detectionMode === item.id }"
        @click="handleSelect(item.id)"
        :title="item.label"
      >
        <el-icon :size="20">
          <component :is="item.icon" />
        </el-icon>
        <div class="nav-content" v-show="isExpanded">
          <span class="nav-label">{{ item.label }}</span>
          <span class="nav-status">{{ item.status }}</span>
        </div>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="nav-item user-item" @click="goLogin" title="用户">
        <el-icon :size="20"><User /></el-icon>
        <span class="nav-label" v-show="isExpanded">
          {{ userStore.isLoggedIn ? userStore.username : '登录' }}
        </span>
      </div>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.sidebar {
  width: 60px;
  background: white;
  border-right: 1px solid #c8e6c9;
  display: flex;
  flex-direction: column;
  padding: 16px 8px;
  transition: all 0.3s ease;

  &.expanded {
    width: 180px;

    .nav-item {
      opacity: 1;
      transform: translateX(0);
      justify-content: flex-start;
      padding: 12px 14px;
      border-radius: 12px;
      margin: 4px 0;
    }

    .nav-content {
      display: flex;
      flex-direction: column;
      margin-left: 12px;
    }
  }
}

.sidebar-header {
  margin-bottom: 20px;
}

.menu-btn {
  width: 44px;
  height: 44px;
  background: #e8f5e9;
  border: none;
  border-radius: 12px;
  color: #5d7a4f;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover {
    background: #4caf50;
    color: white;
    transform: scale(1.05);
  }
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  width: 44px;
  height: 44px;
  background: transparent;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #999;
  position: relative;
  opacity: 0;
  transform: translateX(-10px);

  &:nth-child(n) {
    opacity: 1;
    transform: translateX(0);
  }

  &:hover {
    background: #e8f5e9;
    color: #4caf50;
    transform: translateX(0) scale(1.05);
  }

  &.active {
    background: #4caf50;
    color: white;

    &::after {
      content: '';
      position: absolute;
      left: -8px;
      top: 50%;
      transform: translateY(-50%);
      width: 4px;
      height: 20px;
      background: #4caf50;
      border-radius: 0 4px 4px 0;
    }
  }
}

.nav-content {
  display: none;
}

.nav-label {
  font-size: 13px;
  color: inherit;
  white-space: nowrap;
  font-weight: 500;
}

.nav-status {
  font-size: 10px;
  color: #ccc;
  white-space: nowrap;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #e8f5e9;
}

.user-item {
  opacity: 1 !important;
  transform: translateX(0) !important;
}
</style>

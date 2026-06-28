<script setup lang="ts">
import { useDetectionStore } from '@/stores/detection'

const store = useDetectionStore()

function saveResults() {
  if (store.detectionResults.length === 0) {
    alert('请先进行检测操作！')
    return
  }

  const headers = ['序号', '画面标识', '结果', '位置', '置信度']
  const rows = store.detectionResults.map(r => [
    r.id, r.filePath, r.className,
    r.bbox.join(','), r.confidence
  ])

  let csv = headers.join(',') + '\n'
  rows.forEach(row => { csv += row.join(',') + '\n' })

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `detection_${new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')}.csv`
  link.click()
}
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <button class="header-btn" @click="saveResults" title="保存结果">
        <el-icon><Download /></el-icon>
        <span>保存</span>
      </button>
      <button class="header-btn" title="作者信息">
        <el-icon><User /></el-icon>
        <span>作者</span>
      </button>
      <button class="header-btn" title="版本信息">
        <el-icon><InfoFilled /></el-icon>
        <span>版本</span>
      </button>
    </div>

    <div class="header-center">
      <h1 class="title">基于YOLOv8/v5的农作物害虫检测系统</h1>
    </div>

    <div class="header-right">
      <div class="status-badge" :class="{ active: store.isDetecting }">
        <span class="dot"></span>
        <span class="status-text">{{ store.isDetecting ? '检测中' : '待机' }}</span>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.app-header {
  height: 60px;
  background: white;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  gap: 10px;
}

.header-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f8f8f8;
  border: 1px solid #eee;
  border-radius: 10px;
  color: #666;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #4caf50;
    border-color: #4caf50;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
  }
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.title {
  font-size: 16px;
  font-weight: 700;
  color: #2e3d27;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #e8f5e9;
  border-radius: 20px;
  transition: all 0.3s ease;

  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ccc;
    transition: all 0.3s ease;
  }

  .status-text {
    font-size: 12px;
    color: #999;
    font-weight: 500;
  }

  &.active {
    background: #e8f5e9;

    .dot {
      background: #4caf50;
      box-shadow: 0 0 8px rgba(76, 175, 80, 0.5);
      animation: pulse 1.5s ease-in-out infinite;
    }

    .status-text {
      color: #4caf50;
    }
  }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}
</style>

<script setup lang="ts">
import { computed } from 'vue'
import { useDetectionStore } from '@/stores/detection'
import { useUserStore } from '@/stores/user'

const store = useDetectionStore()
const userStore = useUserStore()

const selectedDet = computed(() => store.selectedDetection)
</script>

<template>
  <aside class="result-panel">
    <div class="panel-header">
      <h2 class="panel-title">检测结果</h2>
    </div>

    <!-- 检测画面预览 -->
    <div class="preview-section">
      <div class="preview-card">
        <img
          v-if="store.currentImage"
          :src="store.currentImage"
          class="preview-image"
          alt="preview"
        />
        <div v-else class="preview-placeholder">
          <el-icon :size="48" color="#ddd"><Picture /></el-icon>
          <span>等待检测</span>
        </div>
      </div>
    </div>

    <!-- 目标选择 -->
    <div class="select-section">
      <el-select
        v-model="store.selectedTarget"
        placeholder="所有目标"
        size="default"
        style="width: 100%"
      >
        <el-option :value="-1" label="所有目标" />
        <el-option
          v-for="(det, index) in store.detections"
          :key="index"
          :value="index"
          :label="`${det.class_name}-${index + 1}`"
        />
      </el-select>
    </div>

    <!-- 检测详情 -->
    <div class="detail-section" v-if="selectedDet">
      <div class="detail-item">
        <span class="detail-label">类别</span>
        <span class="detail-value highlight">{{ selectedDet.class_name }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">置信度</span>
        <span class="detail-value">{{ (selectedDet.score * 100).toFixed(2) }}%</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">位置</span>
      </div>
      <div class="coord-grid">
        <div class="coord-item">
          <span class="coord-label">X1</span>
          <span class="coord-value">{{ selectedDet.bbox[0]?.toFixed(0) || 0 }}</span>
        </div>
        <div class="coord-item">
          <span class="coord-label">Y1</span>
          <span class="coord-value">{{ selectedDet.bbox[1]?.toFixed(0) || 0 }}</span>
        </div>
        <div class="coord-item">
          <span class="coord-label">X2</span>
          <span class="coord-value">{{ selectedDet.bbox[2]?.toFixed(0) || 0 }}</span>
        </div>
        <div class="coord-item">
          <span class="coord-label">Y2</span>
          <span class="coord-value">{{ selectedDet.bbox[3]?.toFixed(0) || 0 }}</span>
        </div>
      </div>
    </div>

    <div class="detail-section empty" v-else>
      <span class="no-data">暂无检测数据</span>
    </div>

    <!-- 用户信息 -->
    <div class="user-section">
      <div class="user-info">
        <div class="user-avatar">
          <el-icon :size="20"><User /></el-icon>
        </div>
        <span class="user-name">{{ userStore.isLoggedIn ? userStore.username : '游客' }}</span>
      </div>
    </div>
  </aside>
</template>

<style scoped lang="scss">
.result-panel {
  width: 320px;
  min-width: 320px;
  max-width: 400px;
  height: 100%;
  background: white;
  border-left: 1px solid #eee;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.panel-header {
  padding: 20px 24px 16px;
  border-bottom: 1px solid #f0f0f0;

  .panel-title {
    font-size: 16px;
    font-weight: 700;
    color: #1a1a1a;
  }
}

.preview-section {
  padding: 16px 24px;
}

.preview-card {
  width: 100%;
  aspect-ratio: 4/3;
  background: #f1f8e9;
  border-radius: 16px;
  border: 1px solid #c8e6c9;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #ccc;
  font-size: 13px;
}

.select-section {
  padding: 0 24px 16px;
}

.detail-section {
  padding: 0 24px 16px;
  flex: 1;

  &.empty {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;

  .detail-label {
    color: #8aa67a;
    font-size: 13px;
    min-width: 50px;
  }

  .detail-value {
    color: #2e3d27;
    font-size: 14px;
    font-weight: 600;

    &.highlight {
      color: #4caf50;
    }
  }
}

.coord-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 8px;
}

.coord-item {
  background: #f1f8e9;
  border-radius: 10px;
  border: 1px solid #c8e6c9;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 8px;

  .coord-label {
    color: #8aa67a;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  .coord-value {
    color: #2e3d27;
    font-size: 13px;
    font-weight: 500;
  }
}

.no-data {
  color: #ccc;
  font-size: 13px;
}

.user-section {
  margin-top: auto;
  padding: 16px 24px;
  border-top: 1px solid #e8f5e9;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.user-name {
  font-size: 14px;
  color: #2e3d27;
  font-weight: 500;
}
</style>

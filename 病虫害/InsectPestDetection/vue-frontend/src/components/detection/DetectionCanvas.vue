<script setup lang="ts">
import { computed } from 'vue'
import { useDetectionStore } from '@/stores/detection'

const store = useDetectionStore()
const hasImage = computed(() => !!store.currentImage)
</script>

<template>
  <div class="detection-canvas">
    <!-- 错误信息 -->
    <div v-if="store.errorMessage" class="error-banner">
      <span class="error-icon">⚠️</span>
      <span class="error-text">{{ store.errorMessage }}</span>
    </div>

    <!-- 检测结果图像 -->
    <img
      v-if="hasImage"
      :src="store.currentImage"
      class="display-image"
      alt="detection result"
    />

    <!-- 占位符 -->
    <div v-else class="canvas-placeholder">
      <div class="placeholder-icon">
        <svg viewBox="0 0 100 100" width="100" height="100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="#f26522" stroke-width="2" opacity="0.3" />
          <circle cx="50" cy="50" r="30" fill="none" stroke="#f26522" stroke-width="1.5" opacity="0.2" />
          <circle cx="50" cy="50" r="15" fill="rgba(242, 101, 34, 0.1)" stroke="#f26522" stroke-width="1" opacity="0.3" />
        </svg>
      </div>
      <h3 class="placeholder-title">选择检测模式开始工作</h3>
      <p class="placeholder-hint">支持图片 / 视频 / 摄像头实时检测</p>
    </div>

    <!-- 进度条 -->
    <div class="progress-bar" v-if="store.isDetecting">
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: store.progress + '%' }"></div>
      </div>
      <span class="progress-text">{{ store.progress.toFixed(1) }}%</span>
    </div>

    <!-- 检测信息叠加层 -->
    <div class="info-overlay" v-if="hasImage">
      <div class="overlay-item">
        <span class="overlay-label">用时</span>
        <span class="overlay-value">{{ store.inferenceTime.toFixed(2) }}s</span>
      </div>
      <div class="overlay-item highlight">
        <span class="overlay-label">目标</span>
        <span class="overlay-value">{{ store.totalCount }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.detection-canvas {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background: #f1f8e9;
  margin: 0 16px;
  border-radius: 20px;
  border: 2px solid #c8e6c9;
  overflow: hidden;
  min-height: 400px;
}

.error-banner {
  position: absolute;
  top: 16px;
  left: 16px;
  right: 16px;
  z-index: 10;
  background: #fff3f3;
  border: 1px solid #ffcdd2;
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.1);
  animation: slideDown 0.3s ease-out;
}

.error-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.error-text {
  color: #d32f2f;
  font-size: 13px;
  line-height: 1.4;
}

@keyframes slideDown {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.display-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  animation: fadeIn 0.3s ease-out;
}

.canvas-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
}

.placeholder-icon {
  animation: float 3s ease-in-out infinite;
}

.placeholder-title {
  font-size: 18px;
  color: #2e3d27;
  font-weight: 600;
}

.placeholder-hint {
  color: #999;
  font-size: 14px;
}

.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(0deg, rgba(255, 255, 255, 0.95), transparent);
}

.progress-track {
  flex: 1;
  height: 4px;
  background: #eee;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #66bb6a);
  transition: width 0.3s ease;
  border-radius: 2px;
}

.progress-text {
  color: #4caf50;
  font-size: 12px;
  font-weight: 600;
  min-width: 45px;
  text-align: right;
}

.info-overlay {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 5;
}

.overlay-item {
  background: white;
  border-radius: 12px;
  border: 1px solid #c8e6c9;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);

  .overlay-label {
    color: #8aa67a;
    font-size: 12px;
  }

  .overlay-value {
    color: #2e3d27;
    font-size: 14px;
    font-weight: 600;
  }

  &.highlight {
    background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);

    .overlay-label,
    .overlay-value {
      color: white;
    }
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>

<script setup lang="ts">
import { useDetectionStore } from '@/stores/detection'

const store = useDetectionStore()

function onConfChange(val: number) {
  store.confThreshold = val
}

function onIouChange(val: number) {
  store.iouThreshold = val
}
</script>

<template>
  <div class="slider-group">
    <div class="slider-item">
      <label class="slider-label">
        <span class="label-text">置信度</span>
        <span class="label-value">{{ (store.confThreshold + 1) / 100 }}</span>
      </label>
      <el-slider
        :model-value="store.confThreshold"
        @update:model-value="onConfChange"
        :min="0"
        :max="99"
        :show-tooltip="false"
      />
    </div>
    <div class="slider-item">
      <label class="slider-label">
        <span class="label-text">IOU</span>
        <span class="label-value">{{ (store.iouThreshold + 1) / 100 }}</span>
      </label>
      <el-slider
        :model-value="store.iouThreshold"
        @update:model-value="onIouChange"
        :min="0"
        :max="99"
        :show-tooltip="false"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.slider-group {
  display: flex;
  gap: 24px;
  padding: 12px 16px;
  background: white;
  margin: 16px 16px 0;
  border-radius: 12px;
  border: 1px solid #c8e6c9;
  box-shadow: 0 2px 10px rgba(76, 175, 80, 0.08);
}

.slider-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slider-label {
  display: flex;
  align-items: center;
  justify-content: space-between;

  .label-text {
    color: #5d7a4f;
    font-size: 13px;
    font-weight: 500;
  }

  .label-value {
    color: #4caf50;
    font-weight: 700;
    font-size: 14px;
  }
}
</style>

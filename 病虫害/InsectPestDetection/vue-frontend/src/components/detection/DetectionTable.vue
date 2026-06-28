<script setup lang="ts">
import { useDetectionStore } from '@/stores/detection'

const store = useDetectionStore()

function handleRowClick(row: any) {
  store.selectedTarget = row.id - 1
}
</script>

<template>
  <div class="detection-table-wrapper">
    <div class="table-header">
      <h3 class="table-title">识别记录</h3>
      <span class="record-count">共 {{ store.detectionResults.length }} 条</span>
    </div>
    <el-table
      :data="store.detectionResults"
      style="width: 100%"
      :row-class-name="() => 'detection-row'"
      :highlight-current-row="true"
      @row-click="handleRowClick"
      max-height="180"
    >
      <el-table-column prop="id" label="序号" width="60" align="center" />
      <el-table-column prop="filePath" label="画面标识" min-width="120" show-overflow-tooltip />
      <el-table-column prop="className" label="结果" min-width="120" />
      <el-table-column label="位置" min-width="140">
        <template #default="{ row }">
          {{ row.bbox.map((v: number) => Math.round(v)).join(', ') }}
        </template>
      </el-table-column>
      <el-table-column prop="confidence" label="置信度" width="80" align="center" />
    </el-table>
  </div>
</template>

<style scoped lang="scss">
.detection-table-wrapper {
  background: white;
  border-radius: 16px;
  margin: 0 16px 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(76, 175, 80, 0.08);
  border: 1px solid #c8e6c9;
}

.table-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e8f5e9;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .table-title {
    font-size: 14px;
    color: #2e3d27;
    font-weight: 600;
  }

  .record-count {
    font-size: 12px;
    color: #8aa67a;
  }
}

:deep(.detection-row) {
  cursor: pointer;
  transition: all 0.15s ease;

  &:hover {
    background: rgba(76, 175, 80, 0.05) !important;
  }
}

:deep(.el-table__current-row) {
  background: rgba(76, 175, 80, 0.08) !important;
}

:deep(.el-table) {
  &::before {
    display: none;
  }

  .el-table__inner-wrapper::before {
    display: none;
  }
}
</style>

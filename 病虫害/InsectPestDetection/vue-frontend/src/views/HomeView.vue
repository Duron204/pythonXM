<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useDetectionStore } from '@/stores/detection'
import { useWebSocket } from '@/composables/useWebSocket'
import AppHeader from '@/components/layout/AppHeader.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import ResultPanel from '@/components/layout/ResultPanel.vue'
import DetectionCanvas from '@/components/detection/DetectionCanvas.vue'
import DetectionTable from '@/components/detection/DetectionTable.vue'
import ConfidenceSlider from '@/components/common/ConfidenceSlider.vue'

const store = useDetectionStore()
const { connect, startDetection, stopDetection, disconnect } = useWebSocket()

const fileInput = ref<HTMLInputElement | null>(null)
const videoInput = ref<HTMLInputElement | null>(null)
const folderInput = ref<HTMLInputElement | null>(null)
const modelInput = ref<HTMLInputElement | null>(null)

/** 在客户端压缩图片，避免发送过大base64数据导致WebSocket超限 */
function compressImage(file: File, maxDimension: number = 640): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => {
      // 计算缩放比例，保持宽高比
      let { width, height } = img
      if (width > maxDimension || height > maxDimension) {
        const ratio = Math.min(maxDimension / width, maxDimension / height)
        width = Math.round(width * ratio)
        height = Math.round(height * ratio)
      }

      // 用canvas缩小图片
      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        reject(new Error('无法创建canvas上下文'))
        return
      }
      ctx.drawImage(img, 0, 0, width, height)

      // 导出为压缩后的JPEG base64（不含 data: 前缀）
      resolve(canvas.toDataURL('image/jpeg', 0.85).split(',')[1])

      // 释放内存
      URL.revokeObjectURL(img.src)
    }
    img.onerror = () => {
      URL.revokeObjectURL(img.src)
      reject(new Error('图片加载失败'))
    }
    img.src = URL.createObjectURL(file)
  })
}

onMounted(() => {
  connect()
})

onUnmounted(() => {
  disconnect()
})

function handleModeSelect(mode: string) {
  if (store.isDetecting) {
    stopDetection()
  }

  switch (mode) {
    case 'image':
      fileInput.value?.click()
      break
    case 'folder':
      folderInput.value?.click()
      break
    case 'video':
      videoInput.value?.click()
      break
    case 'camera':
      startDetection({ mode: 'camera' })
      break
    case 'model':
      modelInput.value?.click()
      break
  }
}

async function handleImageUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  try {
    // 在客户端压缩图片后再通过WebSocket发送
    store.errorMessage = ''
    const base64 = await compressImage(file, 640)
    startDetection({ mode: 'image', imageData: base64 })
  } catch (e) {
    console.error('图片处理失败:', e)
    store.errorMessage = '图片处理失败，请重试'
  }

  input.value = ''
}

function handleVideoUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  startDetection({ mode: 'video', path: file.name })
  input.value = ''
}

function handleFolderUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const files = input.files
  if (!files || files.length === 0) return

  const firstFile = files[0]
  if (firstFile) {
    startDetection({ mode: 'image', path: firstFile.name })
  }
  input.value = ''
}

function handleModelSelect(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  store.modelPath = file.name
  input.value = ''
}
</script>

<template>
  <div class="home-view hex-grid-bg">
    <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="handleImageUpload" />
    <input ref="videoInput" type="file" accept="video/*" style="display:none" @change="handleVideoUpload" />
    <input ref="folderInput" type="file" webkitdirectory style="display:none" @change="handleFolderUpload" />
    <input ref="modelInput" type="file" accept=".pt" style="display:none" @change="handleModelSelect" />

    <AppHeader />

    <div class="main-content">
      <Sidebar @select-mode="handleModeSelect" />

      <div class="center-area">
        <ConfidenceSlider />
        <DetectionCanvas />
        <DetectionTable />
      </div>

      <ResultPanel />
    </div>
  </div>
</template>

<style scoped lang="scss">
.home-view {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.center-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>

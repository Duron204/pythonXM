import { ref, onUnmounted } from 'vue'
import { useDetectionStore } from '@/stores/detection'

export function useWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const store = useDetectionStore()

  function connect() {
    // 连接到独立的WebSocket检测服务器
    ws.value = new WebSocket('ws://127.0.0.1:8765')

    ws.value.onopen = () => {
      isConnected.value = true
      store.errorMessage = ''
      console.log('WebSocket connected')
    }

    ws.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handleMessage(data)
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e)
      }
    }

    ws.value.onclose = (event) => {
      isConnected.value = false
      if (!event.wasClean) {
        store.errorMessage = '连接中断，请检查WebSocket服务器是否运行'
      }
      console.log('WebSocket disconnected', event.code, event.reason)
    }

    ws.value.onerror = () => {
      store.errorMessage = '无法连接检测服务器，请确认已启动: python ws_server.py'
      isConnected.value = false
    }
  }

  function handleMessage(data: any) {
    switch (data.type) {
      case 'frame':
      case 'image_result':
        store.errorMessage = ''
        store.updateDetection(data)
        break
      case 'detection_complete':
        store.isDetecting = false
        break
      case 'error':
        store.errorMessage = data.message || '检测失败'
        store.isDetecting = false
        console.error('Detection error:', data.message)
        break
      case 'status':
        store.isDetecting = data.status === 'detecting'
        if (data.status === 'detecting') {
          store.errorMessage = ''
        }
        break
    }
  }

  function send(data: any) {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(data))
    }
  }

  function startDetection(options: {
    mode: 'image' | 'video' | 'camera'
    path?: string
    fileId?: string
    imageData?: string
  }) {
    store.reset()
    store.isDetecting = true
    store.detectionMode = options.mode

    if (options.mode === 'image' && options.imageData) {
      // 直接发送base64图片数据到WebSocket检测
      send({
        type: 'detect_image',
        image: options.imageData,
        conf: store.confThreshold / 100,
        iou: store.iouThreshold / 100
      })
    } else if (options.mode === 'image' && options.fileId) {
      send({
        type: 'detect_image',
        file_id: options.fileId,
        conf: store.confThreshold / 100,
        iou: store.iouThreshold / 100
      })
    } else {
      send({
        type: 'start_stream',
        mode: options.mode,
        path: options.path || '',
        conf: store.confThreshold / 100,
        iou: store.iouThreshold / 100
      })
    }
  }

  function stopDetection() {
    send({ type: 'stop_stream' })
    store.isDetecting = false
  }

  function updateParams(conf: number, iou: number) {
    send({ type: 'update_params', conf: conf / 100, iou: iou / 100 })
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    connect,
    send,
    startDetection,
    stopDetection,
    updateParams,
    disconnect
  }
}

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Detection {
  class_name: string
  class_id: number
  bbox: number[]
  score: number
}

export interface DetectionResult {
  id: number
  filePath: string
  className: string
  bbox: number[]
  confidence: string
}

export const useDetectionStore = defineStore('detection', () => {
  const currentImage = ref<string>('')
  const detections = ref<Detection[]>([])
  const inferenceTime = ref<number>(0)
  const progress = ref<number>(0)
  const totalFrames = ref<number>(1000)
  const currentFrame = ref<number>(0)
  const isDetecting = ref<boolean>(false)
  const detectionMode = ref<'image' | 'video' | 'camera' | 'folder' | null>(null)
  const errorMessage = ref<string>('')
  const modelPath = ref<string>('weights/best-yolov8n.pt')
  const confThreshold = ref<number>(25)
  const iouThreshold = ref<number>(50)
  const selectedTarget = ref<number>(-1)
  const detectionResults = ref<DetectionResult[]>([])
  const idTab = ref<number>(0)

  const classNames = [
    'Hellula undalis', 'Leaf Webber', 'ash weevil', 'blister beetle',
    'fruit fly', 'fruit sucking moth', 'helicoverpa', 'leucinodes',
    'mealy bug', 'pieris', 'plutella', 'root grubs',
    'schizaphis graminum', 'uroleucon compositae', 'whitefly'
  ]

  const classCounts = computed(() => {
    const counts: Record<string, number> = {}
    classNames.forEach(name => { counts[name] = 0 })
    detections.value.forEach(det => {
      const name = det.class_name
      const current = counts[name]
      if (current !== undefined) {
        counts[name] = current + 1
      }
    })
    return counts
  })

  const totalCount = computed(() => {
    return Object.values(classCounts.value).reduce((sum, count) => sum + count, 0)
  })

  const selectedDetection = computed(() => {
    if (selectedTarget.value === -1 || detections.value.length === 0) {
      return detections.value[0] || null
    }
    return detections.value[selectedTarget.value] || null
  })

  function updateDetection(frameData: {
    image: string
    detections: Detection[]
    inference_time: number
    progress: number
  }) {
    currentImage.value = `data:image/jpeg;base64,${frameData.image}`
    detections.value = frameData.detections
    inferenceTime.value = frameData.inference_time
    progress.value = frameData.progress
    currentFrame.value++

    frameData.detections.forEach(det => {
      idTab.value++
      detectionResults.value.push({
        id: idTab.value,
        filePath: detectionMode.value === 'camera' ? 'Camera 0' : currentImage.value,
        className: det.class_name,
        bbox: det.bbox,
        confidence: (det.score * 100).toFixed(2) + '%'
      })
    })
  }

  function reset() {
    currentImage.value = ''
    detections.value = []
    inferenceTime.value = 0
    progress.value = 0
    currentFrame.value = 0
    selectedTarget.value = -1
    detectionResults.value = []
    idTab.value = 0
    errorMessage.value = ''
  }

  return {
    currentImage,
    detections,
    inferenceTime,
    progress,
    totalFrames,
    currentFrame,
    isDetecting,
    detectionMode,
    errorMessage,
    modelPath,
    confThreshold,
    iouThreshold,
    selectedTarget,
    detectionResults,
    idTab,
    classNames,
    classCounts,
    totalCount,
    selectedDetection,
    updateDetection,
    reset
  }
})

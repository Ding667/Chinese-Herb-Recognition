<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">中草药识别</h2>
      <p class="page-sub">上传中草药图片，系统自动检测并识别药材类别</p>
    </div>

    <div class="recognition-grid">
      <UploadCard ref="uploadRef" :loading="loading" @detect="handleDetect" />
      <ResultCard :result="result" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import UploadCard from '@/components/UploadCard.vue'
import ResultCard from '@/components/ResultCard.vue'
import { detectImage } from '@/api/request'

const loading = ref(false)
const result = ref(null)
const uploadRef = ref(null)

const handleDetect = async (file) => {
  loading.value = true
  result.value = null
  try {
    const res = await detectImage(file)
    if (res && res.data) {
      result.value = res.data
      ElMessage.success(res.message || '检测完成')
    } else {
      ElMessage.warning('未返回检测结果')
    }
  } catch (e) {
    ElMessage.error('检测失败，请重试')
  } finally {
    loading.value = false
    // 检测完成后清空上传状态，支持再次上传
    uploadRef.value?.reset()
  }
}
</script>

<style scoped>
/* 上传区 : 结果区 = 1 : 1，等高 */
.recognition-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: stretch;
}
.recognition-grid > * {
  min-width: 0;
}

/* 响应式换行 */
@media (max-width: 992px) {
  .recognition-grid {
    grid-template-columns: 1fr;
  }
}
</style>

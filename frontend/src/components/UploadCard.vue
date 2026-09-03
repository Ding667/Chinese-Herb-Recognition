<template>
  <el-card class="upload-card" shadow="never">
    <template #header>
      <span class="card-title">图片上传</span>
    </template>

    <el-upload
      ref="uploadRef"
      drag
      :auto-upload="false"
      :show-file-list="false"
      accept=".jpg,.jpeg,.png,.bmp"
      :on-change="handleChange"
      class="upload-area"
    >
      <div v-if="!previewUrl" class="upload-placeholder">
        <el-icon class="upload-icon"><UploadFilled /></el-icon>
        <div class="upload-text">将图片拖到此处，或点击上传</div>
        <div class="upload-tip">支持 JPG / PNG / BMP 格式</div>
      </div>
      <div v-else class="upload-preview">
        <img :src="previewUrl" class="preview-img" alt="预览图" />
      </div>
    </el-upload>

    <div class="upload-actions">
      <el-button
        v-if="previewUrl"
        type="primary"
        :loading="loading"
        style="width: 100%"
        @click="handleDetect"
      >
        {{ loading ? '检测中...' : '开始识别' }}
      </el-button>
      <el-button v-else disabled style="width: 100%">
        请先上传图片
      </el-button>
      <el-button
        v-if="previewUrl && !loading"
        style="width: 100%"
        @click="reset"
      >
        重新上传
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['detect'])

const uploadRef = ref(null)
const file = ref(null)
const previewUrl = ref('')

const handleChange = (uploadFile) => {
  const raw = uploadFile.raw
  if (!raw) return
  // 新文件覆盖旧文件
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  file.value = raw
  previewUrl.value = URL.createObjectURL(raw)
}

const handleDetect = () => {
  if (file.value) {
    emit('detect', file.value)
  }
}

// 清空上传状态，允许再次上传
const reset = () => {
  file.value = null
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = ''
  // 清空 el-upload 内部 fileList，重置 input，确保同一文件可再次选择
  uploadRef.value?.clearFiles()
}

defineExpose({ reset })
</script>

<style scoped>
.upload-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.upload-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.card-title {
  font-weight: 500;
}
.upload-area :deep(.el-upload) {
  width: 100%;
}
.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  padding: 30px 0;
}
.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
}
.upload-text {
  font-size: 14px;
  color: #606266;
}
.upload-tip {
  font-size: 12px;
  color: #909399;
}
.upload-preview {
  display: flex;
  justify-content: center;
  align-items: center;
}
.preview-img {
  max-width: 100%;
  max-height: 240px;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
}
.upload-actions {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>

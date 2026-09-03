<template>
  <el-card class="result-card" shadow="never">
    <template #header>
      <div class="result-header">
        <span class="card-title">检测结果</span>
        <el-tag v-if="result" type="success" effect="plain">
          检测到 {{ result.count }} 个目标
        </el-tag>
      </div>
    </template>

    <div v-if="!result" class="empty-result">
      <el-empty description="暂无检测结果，请先上传图片" />
    </div>

    <div v-else>
      <div class="result-image-wrap">
        <img :src="result.image" class="result-img" alt="检测结果图" />
      </div>
      <el-divider content-position="left">识别明细</el-divider>
      <el-table :data="result.results" size="small" stripe>
        <el-table-column type="index" label="#" width="50" />
        <el-table-column prop="class_name" label="药材类别" min-width="120" />
        <el-table-column label="置信度" min-width="140">
          <template #default="{ row }">
            <el-progress
              :percentage="Math.round(row.confidence * 100)"
              :stroke-width="14"
              :color="progressColor(row.confidence)"
            />
          </template>
        </el-table-column>
        <el-table-column label="边界框坐标" min-width="180">
          <template #default="{ row }">
            <span class="bbox">[{{ row.bbox.map((v) => Math.round(v)).join(', ') }}]</span>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  result: { type: Object, default: null },
})

const progressColor = (conf) => {
  if (conf >= 0.8) return '#67c23a'
  if (conf >= 0.5) return '#e6a23c'
  return '#f56c6c'
}
</script>

<style scoped>
.result-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.result-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-title {
  font-weight: 500;
}
.empty-result {
  padding: 20px 0;
}
.result-image-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #fafafa;
  border-radius: 8px;
  padding: 12px;
  min-height: 200px;
}
.result-img {
  max-width: 100%;
  max-height: 400px;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 6px;
}
.bbox {
  font-family: monospace;
  font-size: 12px;
  color: #909399;
}
</style>

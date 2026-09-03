<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">模型信息</h2>
      <p class="page-sub">YOLOv8n 中草药识别模型配置与性能指标</p>
    </div>

    <!-- 模型基本信息 -->
    <el-card shadow="never" class="base-card">
      <template #header>
        <span class="card-title">模型基本信息</span>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="检测模型">YOLOv8n</el-descriptions-item>
        <el-descriptions-item label="增强策略">Mosaic + MixUp（A1）</el-descriptions-item>
        <el-descriptions-item label="数据集">100 类中草药</el-descriptions-item>
        <el-descriptions-item label="参数量">3.35 M（335 万）</el-descriptions-item>
        <el-descriptions-item label="计算量">14.0 GFLOPs（768×768）</el-descriptions-item>
        <el-descriptions-item label="推理设备">RTX 5060 Laptop GPU</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 性能指标卡片网格 -->
    <div class="metric-grid">
      <MetricCard label="mAP@0.5" value="0.8750" :icon="TrendCharts" icon-bg="#409eff" />
      <MetricCard label="mAP@0.5:0.95" value="0.8729" :icon="DataLine" icon-bg="#409eff" />
      <MetricCard label="Precision" value="0.8364" :icon="CircleCheck" icon-bg="#67c23a" />
      <MetricCard label="Recall" value="0.8253" :icon="Aim" icon-bg="#67c23a" />
      <MetricCard label="Top-1 Accuracy" value="82.57%" :icon="Medal" icon-bg="#e6a23c" />
      <MetricCard label="Top-5 Accuracy" value="87.32%" :icon="Trophy" icon-bg="#e6a23c" />
      <MetricCard label="FPS" value="66.48" :icon="Odometer" icon-bg="#f56c6c" />
      <MetricCard label="平均延迟" value="15.04 ms" :icon="Timer" icon-bg="#f56c6c" />
    </div>
  </div>
</template>

<script setup>
import MetricCard from '@/components/MetricCard.vue'
import {
  TrendCharts,
  DataLine,
  CircleCheck,
  Aim,
  Medal,
  Trophy,
  Odometer,
  Timer,
} from '@element-plus/icons-vue'
</script>

<style scoped>
.base-card {
  margin-bottom: 16px;
}
/* 指标卡片：4 列等宽等高 */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.metric-grid > * {
  min-width: 0;
}

@media (max-width: 992px) {
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">系统概览</h2>
      <p class="page-sub">基于 YOLOv8n 轻量化模型的中草药识别系统运行状态</p>
    </div>

    <!-- 指标卡片：4 等宽等高 -->
    <div class="metric-grid">
      <MetricCard label="检测模型" value="YOLOv8n+A1" :icon="Cpu" icon-bg="#409eff" />
      <MetricCard label="识别类别" value="100 类" :icon="Grid" icon-bg="#67c23a" />
      <MetricCard label="mAP@0.5" value="87.50%" :icon="TrendCharts" icon-bg="#e6a23c" />
      <MetricCard label="推理速度" value="66.48 FPS" :icon="Odometer" icon-bg="#f56c6c" />
    </div>

    <!-- 模型性能雷达图 + 推理流程：50 : 50 -->
    <div class="chart-grid">
      <el-card shadow="never" class="chart-card">
        <template #header>
          <span class="card-title">模型性能指标</span>
        </template>
        <div ref="radarRef" class="chart-box"></div>
      </el-card>
      <el-card shadow="never" class="chart-card">
        <template #header>
          <span class="card-title">推理流程</span>
        </template>
        <div class="flow-steps">
          <div class="flow-node flow-node-input">输入图片</div>
          <div class="flow-arrow">↓</div>
          <div class="flow-node flow-node-detect">YOLO 目标检测</div>
          <div class="flow-arrow">↓</div>
          <div class="flow-node flow-node-output">输出药材类别与置信度</div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import * as echarts from 'echarts'
import MetricCard from '@/components/MetricCard.vue'
import { Cpu, Grid, TrendCharts, Odometer } from '@element-plus/icons-vue'

const radarRef = ref(null)
let chart = null

const initRadar = () => {
  chart = echarts.init(radarRef.value)
  chart.setOption({
    tooltip: {},
    radar: {
      indicator: [
        { name: 'Precision', max: 1 },
        { name: 'Recall', max: 1 },
        { name: 'mAP@0.5', max: 1 },
        { name: 'mAP@0.5:0.95', max: 1 },
      ],
      radius: '65%',
      axisName: { color: '#606266' },
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: [0.8364, 0.8253, 0.8750, 0.8729],
            name: 'YOLOv8n+A1',
            areaStyle: { color: 'rgba(64, 158, 255, 0.3)' },
            lineStyle: { color: '#409eff', width: 2 },
            itemStyle: { color: '#409eff' },
          },
        ],
      },
    ],
  })
}

const handleResize = () => chart && chart.resize()

onMounted(() => {
  initRadar()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (chart) {
    chart.dispose()
    chart = null
  }
})
</script>

<style scoped>
/* 指标卡片：4 等宽等高 */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

/* 图表区域：50 : 50 */
.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 16px;
}
.chart-card {
  min-width: 0;
}
.chart-box {
  height: 320px;
}
.flow-steps {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 40px 0;
}
.flow-node {
  padding: 16px 40px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  text-align: center;
  color: #fff;
  width: 220px;
}
.flow-node-input {
  background: #67c23a;
}
.flow-node-detect {
  background: #409eff;
}
.flow-node-output {
  background: #e6a23c;
}
.flow-arrow {
  font-size: 20px;
  color: #c0c4cc;
  line-height: 1;
}

/* 响应式：窗口缩小时换行 */
@media (max-width: 992px) {
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .chart-grid {
    grid-template-columns: 1fr;
  }
}
</style>

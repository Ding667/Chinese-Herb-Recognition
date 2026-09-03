<template>
  <el-card class="metric-card" shadow="hover">
    <div class="metric-inner">
      <div class="metric-icon" :style="{ background: iconBg }">
        <el-icon :size="22"><component :is="icon" /></el-icon>
      </div>
      <div class="metric-content">
        <div class="metric-label">{{ label }}</div>
        <div class="metric-value">{{ value }}</div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  icon: { type: Object, default: null },
  iconBg: { type: String, default: '#409eff' },
})
</script>

<style scoped>
.metric-card {
  border-radius: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.metric-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 20px 24px;
}
.metric-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}
.metric-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}
.metric-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}
.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}
</style>

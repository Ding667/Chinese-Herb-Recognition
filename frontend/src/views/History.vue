<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">历史识别记录</h2>
      <p class="page-sub">查看历史识别结果，支持删除</p>
    </div>

    <el-card shadow="never">
      <el-table :data="pagedRecords" stripe v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="编号" width="80" />
        <el-table-column label="结果图" width="120">
          <template #default="{ row }">
            <el-image
              :src="resultUrl(row)"
              fit="cover"
              style="width: 80px; height: 60px; border-radius: 6px"
              :preview-src-list="[resultUrl(row)]"
              preview-teleported
            />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="识别时间" width="180" />
        <el-table-column prop="target_count" label="目标数" width="80" />
        <el-table-column label="检测类别" min-width="200">
          <template #default="{ row }">
            <el-tag
              v-for="c in parseClasses(row).slice(0, 3)"
              :key="c.name"
              size="small"
              type="success"
              style="margin-right: 6px"
            >
              {{ c.name }}
            </el-tag>
            <span v-if="parseClasses(row).length > 3" class="more-tag">
              +{{ parseClasses(row).length - 3 }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="最高置信度" width="120">
          <template #default="{ row }">
            <span :style="{ color: confColor(row) }">
              {{ maxConf(row).toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="records.length"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getHistory, deleteHistory } from '@/api/request'

const loading = ref(false)
const records = ref([])
const page = ref(1)
const pageSize = 10

const pagedRecords = computed(() => {
  const start = (page.value - 1) * pageSize
  return records.value.slice(start, start + pageSize)
})

const resultUrl = (row) => `/results/${row.result_image}`

const parseResults = (row) => {
  try {
    return JSON.parse(row.result_json || '[]')
  } catch {
    return []
  }
}

const parseClasses = (row) => {
  const list = parseResults(row)
  return list.map((r) => ({ name: r.class_name, conf: r.confidence }))
}

const maxConf = (row) => {
  const list = parseClasses(row)
  if (list.length === 0) return 0
  return Math.max(...list.map((c) => c.conf))
}

const confColor = (row) => {
  const c = maxConf(row)
  if (c >= 0.8) return '#67c23a'
  if (c >= 0.5) return '#e6a23c'
  return '#f56c6c'
}

const loadHistory = async () => {
  loading.value = true
  try {
    const res = await getHistory()
    records.value = res.data || []
  } catch (e) {
    records.value = []
  } finally {
    loading.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该记录吗？', '提示', { type: 'warning' })
    await deleteHistory(row.id)
    ElMessage.success('删除成功')
    loadHistory()
  } catch (e) {
    // 用户取消
  }
}

onMounted(loadHistory)
</script>

<style scoped>
.more-tag {
  font-size: 12px;
  color: #909399;
}
.pagination-wrap {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>

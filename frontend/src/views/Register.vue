<template>
  <div class="login-page">
    <div class="login-bg"></div>
    <div class="login-container">
      <div class="login-left">
        <h1 class="sys-title">基于 YOLOv8 轻量化模型的中草药智能识别系统</h1>
        <p class="sys-desc">
          融合深度学习目标检测技术，实现 100 类常见中草药的快速、准确识别，
          为中药质检、教学科普与药房管理提供智能化支持。
        </p>
        <div class="feature-list">
          <div class="feature-item">
            <div class="feature-icon">🧠</div>
            <div>
              <div class="feature-title">YOLOv8n 轻量化模型</div>
              <div class="feature-sub">参数量仅 335 万，适合边缘部署</div>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🌿</div>
            <div>
              <div class="feature-title">100 类中草药</div>
              <div class="feature-sub">覆盖常见中药材，mAP@0.5 达 87.5%</div>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📷</div>
            <div>
              <div class="feature-title">计算机视觉技术</div>
              <div class="feature-sub">单张图片实时检测，秒级返回结果</div>
            </div>
          </div>
        </div>
      </div>

      <div class="login-right">
        <el-card class="login-card" shadow="always">
          <div class="login-header">
            <div class="login-logo">🌿</div>
            <div class="login-title">注册账号</div>
            <div class="login-sub">创建账号，开启中草药智能识别</div>
          </div>
          <el-form :model="form" @submit.prevent="handleRegister">
            <el-form-item>
              <el-input
                v-model="form.username"
                placeholder="用户名"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>
            <el-form-item>
              <el-input
                v-model="form.password"
                type="password"
                placeholder="密码"
                size="large"
                show-password
                :prefix-icon="Lock"
              />
            </el-form-item>
            <el-form-item>
              <el-input
                v-model="form.confirm"
                type="password"
                placeholder="确认密码"
                size="large"
                show-password
                :prefix-icon="Lock"
                @keyup.enter="handleRegister"
              />
            </el-form-item>
            <el-button
              type="primary"
              size="large"
              style="width: 100%"
              :loading="loading"
              @click="handleRegister"
            >
              注 册
            </el-button>
          </el-form>
          <div class="login-hint">
            已有账号？
            <span class="register-link" @click="router.push('/login')">返回登录</span>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { register } from '@/api/request'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
  confirm: '',
})

const handleRegister = async () => {
  if (!form.username || !form.password || !form.confirm) {
    ElMessage.warning('请填写完整注册信息')
    return
  }
  if (form.password !== form.confirm) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    await register(form.username, form.password)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    // 错误提示由请求拦截器统一处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.login-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #1f2d3d 0%, #2d4a6b 50%, #409eff 100%);
}
.login-container {
  position: relative;
  z-index: 1;
  width: 920px;
  max-width: 92%;
  display: flex;
  gap: 40px;
  align-items: center;
}
.login-left {
  flex: 1;
  color: #fff;
}
.sys-title {
  font-size: 30px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 16px;
}
.sys-desc {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.8;
  margin-bottom: 32px;
}
.feature-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 14px;
}
.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  line-height: 1;
  flex-shrink: 0;
}
.feature-title {
  font-size: 15px;
  font-weight: 500;
}
.feature-sub {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 2px;
}
.login-right {
  width: 360px;
  flex-shrink: 0;
}
.login-card {
  border-radius: 16px;
  border: none;
}
.login-header {
  text-align: center;
  margin-bottom: 24px;
}
.login-logo {
  font-size: 40px;
  margin-bottom: 8px;
}
.login-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}
.login-sub {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
.login-hint {
  text-align: center;
  font-size: 13px;
  color: #909399;
  margin-top: 16px;
}
.register-link {
  color: #409eff;
  cursor: pointer;
}
.register-link:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .login-left {
    display: none;
  }
  .login-container {
    justify-content: center;
  }
}
</style>

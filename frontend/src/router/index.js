import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { blank: true, title: '登录' },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { blank: true, title: '注册' },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '首页' },
  },
  {
    path: '/recognition',
    name: 'Recognition',
    component: () => import('@/views/Recognition.vue'),
    meta: { title: '中草药识别' },
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
    meta: { title: '历史记录' },
  },
  {
    path: '/model',
    name: 'ModelInfo',
    component: () => import('@/views/ModelInfo.vue'),
    meta: { title: '模型信息' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫：未登录跳转登录页（登录/注册页放行）
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('herb_token')
  if (to.path !== '/login' && to.path !== '/register' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router

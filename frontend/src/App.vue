<template>
  <router-view v-if="isBlank" />
  <div v-else class="layout">
    <Sidebar />
    <main class="content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const route = useRoute()
const isBlank = computed(() => !!route.meta.blank)
</script>

<style scoped>
.layout {
  display: flex;
  height: 100%;
  overflow: hidden;
}
.content {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  background: var(--bg-page, #f5f7fa);
}
</style>

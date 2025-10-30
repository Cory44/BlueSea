<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    <TopBar />
    <Toast position="bottom-right" />
    <main class="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-12 px-4 py-12 sm:px-6 lg:px-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import TopBar from '@/components/TopBar.vue';
import Toast from 'primevue/toast';
</script>

<template>
  <div
    class="flex flex-col items-center gap-5 rounded-2xl border border-cyan-100/70 bg-white/80 p-10 text-center shadow-inner transition-colors dark:border-cyan-500/30 dark:bg-slate-900/80"
  >
    <span
      class="flex h-16 w-16 items-center justify-center rounded-full bg-cyan-100 text-cyan-600 shadow-md shadow-cyan-100/50 dark:bg-cyan-500/20 dark:text-cyan-200"
    >
      <i :class="['pi text-3xl', icon]"></i>
    </span>
    <div class="space-y-2">
      <h3 class="text-xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">{{ title }}</h3>
      <p class="max-w-md text-sm leading-relaxed text-slate-600 dark:text-slate-300">{{ description }}</p>
    </div>
    <div v-if="$slots.default" class="flex flex-wrap justify-center gap-3">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: string;
  title: string;
  description: string;
}>();
</script>

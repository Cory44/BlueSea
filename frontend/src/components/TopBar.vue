<template>
  <header class="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
    <div class="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <RouterLink to="/" class="flex items-center gap-3">
        <img class="h-16 w-auto dark:hidden" src="/assets/logo-dark.png" alt="BlueSea logo" />
        <img class="hidden h-16 w-auto dark:block" src="/assets/logo-title-light.png" alt="BlueSea logo" />
      </RouterLink>
      <div class="flex items-center gap-3">
        <Button class="hidden sm:inline-flex" label="Sign in" severity="secondary" text />
        <Button label="Register" severity="primary" />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import Button from 'primevue/button';
</script>

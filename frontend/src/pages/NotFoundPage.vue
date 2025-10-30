<template>
  <section class="mx-auto flex min-h-[60vh] w-full max-w-3xl flex-col items-center justify-center gap-10 text-center">
    <EmptyState
      icon="pi pi-ship"
      title="You drifted off course"
      description="The page you're looking for has sailed beyond our horizon. Try heading back to the shoreline."
      class="w-full bg-bluesea-50/70"
    >
      <RouterLink :to="{ name: 'home' }">
        <Button label="Return home" icon="pi pi-home" />
      </RouterLink>
      <RouterLink :to="{ name: 'feed' }">
        <Button label="View feed" icon="pi pi-compass" severity="secondary" text />
      </RouterLink>
    </EmptyState>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import Button from 'primevue/button';
import EmptyState from '@/components/EmptyState.vue';
</script>

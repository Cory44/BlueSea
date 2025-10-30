<template>
  <section class="mx-auto flex w-full max-w-3xl flex-col gap-8">
    <header class="space-y-3 rounded-3xl bg-white/80 p-8 shadow-md shadow-bluesea-100/40 backdrop-blur dark:bg-slate-900/70">
      <p class="text-sm font-semibold uppercase tracking-[0.35em] text-bluesea-500">Share a sighting</p>
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Create a new post</h1>
      <p class="text-slate-500 dark:text-slate-300">
        Upload a photo with a caption and tags to let others discover your corner of the ocean.
      </p>
    </header>

    <NewPostForm @success="handleSuccess" />
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import NewPostForm from '@/components/NewPostForm.vue';
import { useFeedStore } from '@/stores/feed';

const router = useRouter();
const feedStore = useFeedStore();

const handleSuccess = () => {
  feedStore.triggerRefresh();
  router.push({ name: 'feed' });
};
</script>

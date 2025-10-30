<template>
  <section class="mx-auto flex w-full max-w-3xl flex-col gap-8">
    <header class="space-y-2">
      <h1 class="text-3xl font-semibold">Create a new post</h1>
      <p class="text-slate-500">Share a photo with a caption and tags to let others discover it.</p>
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

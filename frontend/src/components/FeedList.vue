<template>
  <div class="space-y-6">
    <TransitionGroup name="fade" tag="div" class="space-y-6">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </TransitionGroup>

    <div
      v-if="!posts.length && !loading"
      class="rounded-3xl border border-dashed border-bluesea-200 bg-bluesea-50/50 p-8 text-center text-slate-500 backdrop-blur dark:border-bluesea-500/30 dark:bg-slate-900/60"
    >
      <slot name="empty">No posts to display yet.</slot>
    </div>

    <div v-if="loading" class="flex justify-center">
      <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" />
    </div>

    <div v-if="hasMore && !loading" class="flex justify-center">
      <Button label="Load more" @click="onLoadMore" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from 'vue';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import PostCard, { type PostSummary } from './PostCard.vue';

const props = withDefaults(
  defineProps<{
    posts: PostSummary[];
    loading?: boolean;
    hasMore?: boolean;
  }>(),
  {
    loading: false,
    hasMore: false
  }
);

const emit = defineEmits<{ (e: 'load-more'): void }>();

const onLoadMore = () => {
  emit('load-more');
};

const { posts, loading, hasMore } = toRefs(props);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

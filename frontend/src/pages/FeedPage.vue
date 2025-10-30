<template>
  <section class="space-y-8">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-semibold">Your feed</h1>
        <p class="text-slate-500">Catch up with the latest posts across your communities.</p>
      </div>
      <SourceFilter v-model="selectedSource" />
    </header>

    <Message v-if="error" severity="error" :closable="false">
      <div class="flex flex-col gap-2">
        <span>{{ error }}</span>
        <Button label="Retry" severity="secondary" size="small" @click="refresh" />
      </div>
    </Message>

    <FeedList
      :posts="posts"
      :loading="loading"
      :has-more="showLoadMore"
      @load-more="loadMore"
    >
      <template #empty>
        <div class="space-y-3">
          <p>No posts found for this source yet.</p>
          <Button label="Refresh" text severity="secondary" @click="refresh" />
        </div>
      </template>
    </FeedList>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { isAxiosError } from 'axios';
import Button from 'primevue/button';
import Message from 'primevue/message';
import FeedList from '@/components/FeedList.vue';
import SourceFilter from '@/components/SourceFilter.vue';
import type { PostSummary } from '@/components/PostCard.vue';
import api from '@/services/api';

interface FeedResponse {
  items: PostSummary[];
  nextOffset: number | null;
  limit: number;
  offset: number;
}

const posts = ref<PostSummary[]>([]);
const loading = ref(false);
const error = ref('');
const nextOffset = ref<number | null>(null);
const selectedSource = ref<string | null>(null);
const showLoadMore = computed(() => nextOffset.value !== null && posts.value.length > 0);

const fetchPosts = async (reset = false) => {
  if (loading.value) {
    return;
  }

  loading.value = true;
  error.value = '';

  if (reset) {
    posts.value = [];
    nextOffset.value = null;
  }

  const params: Record<string, unknown> = {
    limit: 10
  };

  if (!reset && nextOffset.value) {
    params.offset = nextOffset.value;
  }

  if (reset) {
    params.offset = 0;
  }

  if (selectedSource.value) {
    params.source = selectedSource.value;
  }

  try {
    const { data } = await api.get<FeedResponse>('/posts', { params });
    posts.value = reset ? data.items : [...posts.value, ...data.items];
    nextOffset.value = data.nextOffset ?? null;
  } catch (err) {
    error.value = extractErrorMessage(err);
  } finally {
    loading.value = false;
  }
};

const loadMore = () => {
  if (nextOffset.value === null) {
    return;
  }
  fetchPosts(false);
};

const refresh = () => fetchPosts(true);

onMounted(() => {
  fetchPosts(true);
});

watch(selectedSource, () => {
  fetchPosts(true);
});

const extractErrorMessage = (err: unknown) => {
  if (isAxiosError(err)) {
    const response = err.response;
    const message =
      typeof response?.data === 'object' && response?.data !== null && 'message' in response.data
        ? String((response.data as { message: string }).message)
        : null;

    return message ?? 'Unable to load posts. Please try again later.';
  }

  if (err instanceof Error) {
    return err.message;
  }

  return 'Unable to load posts. Please try again later.';
};
</script>

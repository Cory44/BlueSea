<template>
  <section class="space-y-10">
    <header class="flex flex-col gap-4 rounded-3xl bg-white/70 p-6 shadow-sm backdrop-blur dark:bg-slate-900/60 sm:flex-row sm:items-center sm:justify-between">
      <div class="space-y-1">
        <p class="text-sm font-semibold uppercase tracking-[0.3em] text-bluesea-500">Tide tracker</p>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Your feed</h1>
        <p class="text-slate-500 dark:text-slate-300">Catch up with the latest posts across your communities.</p>
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
        <EmptyState
          icon="pi pi-compass"
          title="The tide is calm"
          description="We couldn't find any posts for this source yet. Try refreshing the feed or exploring another current."
          class="bg-bluesea-50/60"
        >
          <Button label="Refresh" text severity="secondary" @click="refresh" />
        </EmptyState>
      </template>
    </FeedList>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { isAxiosError } from 'axios';
import { useToast } from 'primevue/usetoast';
import Button from 'primevue/button';
import Message from 'primevue/message';
import FeedList from '@/components/FeedList.vue';
import SourceFilter from '@/components/SourceFilter.vue';
import type { PostSummary } from '@/components/PostCard.vue';
import api from '@/services/api';
import { storeToRefs } from 'pinia';
import { useFeedStore } from '@/stores/feed';
import EmptyState from '@/components/EmptyState.vue';

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
const feedStore = useFeedStore();
const { refreshToken } = storeToRefs(feedStore);
const toast = useToast();

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
    toast.add({
      severity: 'error',
      summary: 'Feed unavailable',
      detail: error.value,
      life: 5000
    });
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

watch(refreshToken, () => {
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

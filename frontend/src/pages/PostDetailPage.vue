<template>
  <section class="space-y-6 rounded-3xl bg-white/80 p-6 shadow-sm backdrop-blur dark:bg-slate-900/70">
    <Button label="Back to feed" icon="pi pi-arrow-left" text @click="goBack" />

    <Message v-if="error" severity="error" :closable="false">
      <div class="flex flex-col gap-2">
        <span>{{ error }}</span>
        <Button label="Retry" severity="secondary" size="small" @click="fetchPost" />
      </div>
    </Message>

    <ProgressSpinner v-if="loading" style="width: 50px; height: 50px" strokeWidth="4" class="mx-auto" />

    <PostCard v-if="post && !loading" :post="post" />
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { isAxiosError } from 'axios';
import { useToast } from 'primevue/usetoast';
import Button from 'primevue/button';
import Message from 'primevue/message';
import ProgressSpinner from 'primevue/progressspinner';
import PostCard, { type PostSummary } from '@/components/PostCard.vue';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const post = ref<PostSummary | null>(null);
const loading = ref(false);
const error = ref('');

const goBack = () => {
  router.push({ name: 'feed' });
};

const fetchPost = async () => {
  const id = Number(route.params.id);
  if (!Number.isFinite(id)) {
    error.value = 'Invalid post identifier.';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const { data } = await api.get<{ post: PostSummary }>(`/posts/${id}`);
    post.value = data.post;
  } catch (err) {
    if (isAxiosError(err)) {
      const response = err.response;
      const message =
        typeof response?.data === 'object' && response?.data !== null && 'message' in response.data
          ? String((response.data as { message: string }).message)
          : null;
      error.value = message ?? 'Unable to load this post.';
    } else if (err instanceof Error) {
      error.value = err.message;
    } else {
      error.value = 'Unable to load this post.';
    }
    toast.add({ severity: 'error', summary: 'Post unavailable', detail: error.value, life: 5000 });
  } finally {
    loading.value = false;
  }
};

onMounted(fetchPost);
</script>

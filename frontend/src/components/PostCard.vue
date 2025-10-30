<template>
  <article class="rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
    <div class="flex flex-col gap-4 p-6">
      <header class="flex items-start justify-between gap-4">
        <div>
          <h2 class="text-xl font-semibold text-slate-900 dark:text-white">{{ post.title }}</h2>
          <p class="text-sm text-slate-500">
            <span v-if="post.user">@{{ post.user.username }}</span>
            <span v-else>Unknown author</span>
            <span class="mx-2">•</span>
            <span class="capitalize">{{ post.source }}</span>
            <span v-if="formattedDate"> • {{ formattedDate }}</span>
          </p>
        </div>
        <Tag v-if="post.tags.length" :value="post.tags[0]" class="uppercase" />
      </header>

      <p class="text-base leading-7 text-slate-700 dark:text-slate-200 whitespace-pre-line">
        {{ post.body }}
      </p>

      <img
        v-if="post.image_url"
        :src="post.image_url"
        :alt="`Image for post ${post.title}`"
        class="max-h-96 w-full rounded-xl object-cover"
      />

      <footer v-if="post.tags.length > 1" class="flex flex-wrap gap-2">
        <Tag
          v-for="tag in post.tags.slice(1)"
          :key="tag"
          :value="tag"
          severity="secondary"
          rounded
        />
      </footer>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import Tag from 'primevue/tag';
import type { AuthUser } from '@/stores/auth';

export interface PostSummary {
  id: number;
  title: string;
  body: string;
  source: string;
  tags: string[];
  image_url?: string | null;
  created_at?: string | null;
  user?: AuthUser | null;
}

const props = defineProps<{ post: PostSummary }>();

const formattedDate = computed(() => {
  if (!props.post.created_at) {
    return '';
  }

  const date = new Date(props.post.created_at);
  if (Number.isNaN(date.getTime())) {
    return '';
  }

  return date.toLocaleString();
});
</script>

<template>
  <Card class="!bg-white/80 !text-slate-900 shadow-lg shadow-bluesea-100/30 backdrop-blur dark:!bg-slate-900/80">
    <template #title>
      Share something new
    </template>
    <template #content>
      <form class="space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-2">
          <label for="title" class="block text-sm font-medium text-slate-700 dark:text-slate-200">
            Title
          </label>
          <InputText
            id="title"
            v-model="title"
            placeholder="Give your post a catchy title"
            :disabled="submitting"
            class="w-full !bg-white !text-slate-900"
          />
        </div>

        <div class="space-y-2">
          <label for="description" class="block text-sm font-medium text-slate-700 dark:text-slate-200">
            Description
          </label>
          <Textarea
            id="description"
            v-model="description"
            rows="5"
            placeholder="Tell the story behind this image"
            auto-resize
            :disabled="submitting"
            class="w-full !bg-white !text-slate-900"
          />
        </div>

        <div class="space-y-2">
          <label for="tags" class="block text-sm font-medium text-slate-700 dark:text-slate-200">
            Tags
          </label>
          <Chips
            id="tags"
            v-model="tagChips"
            separator="," 
            :disabled="submitting"
            placeholder="Add tags and press enter"
            class="w-full !bg-white !text-slate-900"
            :pt="{ 
              input: { class: '!bg-white !text-slate-900' },
              container: { class: '!bg-white !text-slate-900' }
            }"
          />
          <p class="text-xs text-slate-500">Use tags to help others discover your post.</p>
        </div>

        <div class="space-y-3">
          <label for="image" class="block text-sm font-medium text-slate-700 dark:text-slate-200">
            Image
          </label>
          <FileUpload
            ref="fileUploadRef"
            mode="basic"
            name="image"
            choose-label="Select image"
            accept="image/*"
            :disabled="submitting"
            :max-file-size="maxFileSize"
            @select="onFileSelect"
            @clear="onClearFile"
          />
          <p class="text-xs text-slate-500">PNG, JPG or GIF up to 5MB.</p>

          <EmptyState
            v-if="!selectedFile"
            icon="pi pi-image"
            title="No image selected"
            description="Choose a marine moment to upload. We'll preview it here so you can fine-tune the details before sharing."
            class="w-full border-dashed border-bluesea-200 bg-bluesea-50/70 py-8 dark:border-bluesea-500/40 dark:bg-slate-900/60"
          />

          <div v-if="previewUrl" class="relative mt-4 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-700">
            <Image :src="previewUrl" alt="Selected image preview" preview image-class="max-h-[400px] w-full object-cover" />
            <Button
              class="absolute right-4 top-4"
              type="button"
              icon="pi pi-times"
              rounded
              text
              severity="secondary"
              @click="removeImage"
            />
          </div>
        </div>

        <div class="flex items-center justify-end gap-3">
          <Button type="button" label="Reset" severity="secondary" text :disabled="submitting" @click="resetForm" />
          <Button type="submit" label="Publish" :loading="submitting" :disabled="isSubmitDisabled" />
        </div>
      </form>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue';
import { isAxiosError } from 'axios';
import { useToast } from 'primevue/usetoast';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Chips from 'primevue/chips';
import FileUpload from 'primevue/fileupload';
import Image from 'primevue/image';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import api from '@/services/api';
import EmptyState from '@/components/EmptyState.vue';

const emit = defineEmits<{ (e: 'success'): void }>();

interface FileUploadSelectEvent {
  files: File[];
}

const title = ref('');
const description = ref('');
const tagChips = ref<string[]>([]);
const submitting = ref(false);
const selectedFile = ref<File | null>(null);
const previewUrl = ref<string | null>(null);
const maxFileSize = 5 * 1024 * 1024;
const toast = useToast();
const fileUploadRef = ref<{ clear: () => void } | null>(null);

const isSubmitDisabled = computed(() => {
  return submitting.value || !title.value.trim() || !description.value.trim() || !selectedFile.value;
});

const revokePreview = () => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
    previewUrl.value = null;
  }
};

const setFile = (file: File | null) => {
  if (selectedFile.value === file) {
    return;
  }
  revokePreview();
  selectedFile.value = file;
  if (file) {
    previewUrl.value = URL.createObjectURL(file);
  }
};

const onFileSelect = (event: FileUploadSelectEvent) => {
  const file = event.files?.[0] ?? null;
  if (!file) {
    setFile(null);
    return;
  }

  if (!file.type.startsWith('image/')) {
    toast.add({
      severity: 'warn',
      summary: 'Unsupported file',
      detail: 'Please choose an image file.',
      life: 4000
    });
    if (fileUploadRef.value) {
      fileUploadRef.value.clear();
    }
    return;
  }

  if (file.size > maxFileSize) {
    toast.add({
      severity: 'warn',
      summary: 'File too large',
      detail: 'Please select an image under 5MB.',
      life: 4000
    });
    if (fileUploadRef.value) {
      fileUploadRef.value.clear();
    }
    return;
  }

  setFile(file);
};

const onClearFile = () => {
  setFile(null);
};

const removeImage = () => {
  if (fileUploadRef.value) {
    fileUploadRef.value.clear();
  }
  setFile(null);
};

const resetForm = () => {
  title.value = '';
  description.value = '';
  tagChips.value = [];
  removeImage();
};

const extractErrorMessage = (error: unknown) => {
  if (isAxiosError(error)) {
    const response = error.response;
    if (response?.data && typeof response.data === 'object' && 'message' in response.data) {
      return String((response.data as { message?: string }).message ?? 'Unable to create the post.');
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'Unable to create the post. Please try again later.';
};

const handleSubmit = async () => {
  if (isSubmitDisabled.value) {
    toast.add({ severity: 'warn', summary: 'Missing information', detail: 'Add a title, description, and image.', life: 3000 });
    return;
  }

  submitting.value = true;

  try {
    const formData = new FormData();
    formData.append('title', title.value.trim());
    formData.append('body', description.value.trim());
    formData.append('source', 'community');
    if (selectedFile.value) {
      formData.append('image', selectedFile.value);
    }

    tagChips.value
      .map((tag) => tag.trim())
      .filter((tag) => tag.length > 0)
      .forEach((tag) => {
        formData.append('tags[]', tag);
      });

    await api.post('/posts', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    toast.add({ severity: 'success', summary: 'Post created', detail: 'Your post has been published.', life: 4000 });
    resetForm();
    emit('success');
  } catch (error) {
    const message = extractErrorMessage(error);
    toast.add({ severity: 'error', summary: 'Could not create post', detail: message, life: 5000 });
  } finally {
    submitting.value = false;
  }
};

onUnmounted(() => {
  revokePreview();
});
</script>

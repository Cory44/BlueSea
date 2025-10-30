<template>
  <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-3">
    <label class="text-sm font-medium text-slate-600 dark:text-slate-300">Source</label>
    <Dropdown
      :model-value="modelValue || ''"
      :options="optionsToUse"
      optionLabel="label"
      optionValue="value"
      placeholder="All sources"
      showClear
      class="w-full sm:w-64"
      @update:modelValue="onUpdate"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import Dropdown from 'primevue/dropdown';

interface SourceOption {
  label: string;
  value: string;
}

const props = withDefaults(
  defineProps<{
    modelValue?: string | null;
    options?: SourceOption[];
  }>(),
  {
    modelValue: '',
    options: () => []
  }
);

const emit = defineEmits<{ (e: 'update:modelValue', value: string | null): void }>();

const defaultOptions: SourceOption[] = [
  { label: 'All sources', value: '' },
  { label: 'Community', value: 'community' },
  { label: 'Global', value: 'global' },
  { label: 'Personal', value: 'personal' }
];

const optionsToUse = computed(() => (props.options.length ? props.options : defaultOptions));

const onUpdate = (value: string | null) => {
  const normalized = value === '' ? null : value;
  emit('update:modelValue', normalized);
};
</script>

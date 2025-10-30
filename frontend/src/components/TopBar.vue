<template>
  <header class="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
    <div class="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <RouterLink to="/" class="flex items-center gap-3">
        <img class="h-16 w-auto dark:hidden" src="/assets/logo-dark.png" alt="BlueSea logo" />
        <img class="hidden h-16 w-auto dark:block" src="/assets/logo-title-light.png" alt="BlueSea logo" />
      </RouterLink>
      <div class="flex items-center gap-3">
        <div v-if="isAuthenticated" class="hidden items-center gap-3 sm:flex">
          <Button label="Feed" severity="secondary" text @click="goToFeed" />
          <Button label="New post" icon="pi pi-plus" @click="goToNewPost" />
          <span class="text-sm text-slate-500 dark:text-slate-300">@{{ username }}</span>
        </div>
        <Button
          v-if="isAuthenticated"
          label="Sign out"
          severity="secondary"
          outlined
          @click="handleLogout"
        />
        <template v-else>
          <Button class="hidden sm:inline-flex" label="Sign in" severity="secondary" text @click="goToLogin" />
          <Button label="Register" severity="primary" @click="goToRegister" />
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import Button from 'primevue/button';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const auth = useAuthStore();

const isAuthenticated = computed(() => auth.isAuthenticated);
const username = computed(() => auth.user?.username ?? '');

const goToLogin = () => {
  router.push({ name: 'login' });
};

const goToRegister = () => {
  router.push({ name: 'register' });
};

const goToFeed = () => {
  router.push({ name: 'feed' });
};

const goToNewPost = () => {
  router.push({ name: 'new-post' });
};

const handleLogout = () => {
  auth.logout();
  router.push({ name: 'home' });
};
</script>

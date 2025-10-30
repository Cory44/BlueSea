<template>
  <section class="flex flex-col items-center justify-center min-h-[calc(100vh-16rem)] gap-12 text-center">
    <div class="max-w-3xl space-y-8">
      <div class="flex justify-center">
        <img class="h-96 w-auto dark:hidden" src="/assets/logo-title-dark.png" alt="BlueSea logo" />
        <img class="hidden h-96 w-auto dark:block" src="/assets/logo-title-light.png" alt="BlueSea logo" />
      </div>
      
      <div class="space-y-6">
        <h1 class="text-5xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-6xl">
          Dive into the conversation
        </h1>
        <p class="text-xl text-slate-600 dark:text-slate-300">
          BlueSea is a decentralized social network where your voice matters. Connect, share, and ride the waves of meaningful conversations.
        </p>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-4 pt-4">
        <Button
          v-if="!isAuthenticated"
          label="Sign in"
          severity="secondary"
          size="large"
          outlined
          class="min-w-[140px]"
          @click="goToLogin"
        />
        <Button
          v-if="!isAuthenticated"
          label="Register"
          severity="primary"
          size="large"
          class="min-w-[140px]"
          @click="goToRegister"
        />
        <Button
          v-else
          label="Go to feed"
          severity="primary"
          size="large"
          class="min-w-[140px]"
          @click="goToFeed"
        />
      </div>

      <div class="pt-8">
        <p class="text-sm text-slate-500 dark:text-slate-400">
          Powered by the AT Protocol • Decentralized • Open Source
        </p>
      </div>
    </div>

    <div class="grid gap-8 pt-12 md:grid-cols-3 max-w-5xl w-full">
      <div class="space-y-3">
        <div class="text-4xl">🌊</div>
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Decentralized</h2>
        <p class="text-slate-600 dark:text-slate-300">
          Your data, your rules. Choose your server or host your own.
        </p>
      </div>
      <div class="space-y-3">
        <div class="text-4xl">🐠</div>
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Open & Free</h2>
        <p class="text-slate-600 dark:text-slate-300">
          Built on open protocols. No algorithms controlling what you see.
        </p>
      </div>
      <div class="space-y-3">
        <div class="text-4xl">⚓</div>
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Community-Driven</h2>
        <p class="text-slate-600 dark:text-slate-300">
          Connect with communities that share your interests and values.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const auth = useAuthStore();

const isAuthenticated = computed(() => auth.isAuthenticated);

const goToLogin = () => {
  router.push({ name: 'login' });
};

const goToRegister = () => {
  router.push({ name: 'register' });
};

const goToFeed = () => {
  router.push({ name: 'feed' });
};
</script>

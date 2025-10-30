<template>
  <section class="mx-auto flex w-full max-w-md flex-col gap-6 rounded-3xl bg-white/85 p-10 shadow-xl shadow-cyan-100/40 backdrop-blur dark:bg-slate-900/70">
    <div class="text-center space-y-2">
      <p class="text-sm font-semibold uppercase tracking-[0.35em] text-cyan-500">Welcome back</p>
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Sign in</h1>
      <p class="text-slate-500 dark:text-slate-300">Access your BlueSea account to dive into the feed.</p>
    </div>

    <Message v-if="formErrors.general" severity="error" :closable="false">{{ formErrors.general }}</Message>

    <form class="space-y-5" @submit.prevent="handleSubmit">
      <div class="space-y-2">
        <label for="username" class="block text-sm font-medium text-slate-700 dark:text-slate-200">Username</label>
        <InputText
          id="username"
          v-model.trim="username"
          type="text"
          autocomplete="username"
          placeholder="you@example.com"
          class="w-full !bg-white !text-slate-900"
          :class="{ 'p-invalid': formErrors.username }"
        />
        <InlineMessage v-if="formErrors.username" severity="error">{{ formErrors.username }}</InlineMessage>
      </div>

      <div class="space-y-2">
        <label for="password" class="block text-sm font-medium text-slate-700 dark:text-slate-200">Password</label>
        <Password
          id="password"
          v-model="password"
          toggleMask
          :feedback="false"
          autocomplete="current-password"
          placeholder="Enter your password"
          class="w-full"
          :input-class="['w-full !bg-white !text-slate-900', { 'p-invalid': formErrors.password }]"
        />
        <InlineMessage v-if="formErrors.password" severity="error">{{ formErrors.password }}</InlineMessage>
      </div>

      <Button type="submit" label="Sign in" class="w-full" :loading="isSubmitting" />
    </form>

    <p class="text-center text-sm text-slate-500">
      Don't have an account?
      <RouterLink class="font-semibold text-primary" :to="{ name: 'register' }">Register now</RouterLink>.
    </p>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useRouter, useRoute, RouterLink } from 'vue-router';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Message from 'primevue/message';
import InlineMessage from 'primevue/inlinemessage';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();
const toast = useToast();

const username = ref('');
const password = ref('');

const formErrors = reactive({
  username: '',
  password: '',
  general: ''
});

const isSubmitting = computed(() => auth.loading);

const validate = () => {
  formErrors.username = '';
  formErrors.password = '';
  formErrors.general = '';

  if (!username.value) {
    formErrors.username = 'Username is required.';
  }

  if (!password.value) {
    formErrors.password = 'Password is required.';
  }

  return !formErrors.username && !formErrors.password;
};

const handleSubmit = async () => {
  if (!validate()) {
    return;
  }

  try {
    await auth.login({ username: username.value, password: password.value });
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/feed';
    toast.add({ severity: 'success', summary: 'Signed in', detail: 'Welcome back to BlueSea!', life: 3000 });
    router.push(redirect);
  } catch (error) {
    formErrors.general = (error as Error).message;
    toast.add({ severity: 'error', summary: 'Sign-in failed', detail: formErrors.general, life: 5000 });
  }
};
</script>

<template>
  <section class="mx-auto flex w-full max-w-md flex-col gap-6 rounded-3xl bg-white/85 p-10 shadow-xl shadow-bluesea-100/40 backdrop-blur dark:bg-slate-900/70">
    <div class="text-center space-y-2">
      <p class="text-sm font-semibold uppercase tracking-[0.35em] text-bluesea-500">Join the crew</p>
      <h1 class="text-3xl font-bold text-slate-900 dark:text-white">Create your account</h1>
      <p class="text-slate-500 dark:text-slate-300">Join BlueSea and start sharing your voice.</p>
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
          autocomplete="new-password"
          placeholder="Create a password"
          class="w-full"
          :input-class="['w-full !bg-white !text-slate-900', { 'p-invalid': formErrors.password }]"
        />
        <InlineMessage v-if="formErrors.password" severity="error">{{ formErrors.password }}</InlineMessage>
      </div>

      <div class="space-y-2">
        <label for="confirmPassword" class="block text-sm font-medium text-slate-700 dark:text-slate-200">Confirm password</label>
        <Password
          id="confirmPassword"
          v-model="confirmPassword"
          toggleMask
          :feedback="false"
          autocomplete="new-password"
          placeholder="Re-enter your password"
          class="w-full"
          :input-class="['w-full !bg-white !text-slate-900', { 'p-invalid': formErrors.confirmPassword }]"
        />
        <InlineMessage v-if="formErrors.confirmPassword" severity="error">{{ formErrors.confirmPassword }}</InlineMessage>
      </div>

      <Button type="submit" label="Register" class="w-full" :loading="isSubmitting" />
    </form>

    <p class="text-center text-sm text-slate-500">
      Already have an account?
      <RouterLink class="font-semibold text-primary" :to="{ name: 'login' }">Sign in</RouterLink>.
    </p>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Message from 'primevue/message';
import InlineMessage from 'primevue/inlinemessage';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const auth = useAuthStore();
const toast = useToast();

const username = ref('');
const password = ref('');
const confirmPassword = ref('');

const formErrors = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  general: ''
});

const isSubmitting = computed(() => auth.loading);

const validate = () => {
  formErrors.username = '';
  formErrors.password = '';
  formErrors.confirmPassword = '';
  formErrors.general = '';

  if (!username.value) {
    formErrors.username = 'Username is required.';
  }

  if (!password.value) {
    formErrors.password = 'Password is required.';
  } else if (password.value.length < 8) {
    formErrors.password = 'Password must be at least 8 characters long.';
  }

  if (!confirmPassword.value) {
    formErrors.confirmPassword = 'Please confirm your password.';
  } else if (confirmPassword.value !== password.value) {
    formErrors.confirmPassword = 'Passwords do not match.';
  }

  return !formErrors.username && !formErrors.password && !formErrors.confirmPassword;
};

const handleSubmit = async () => {
  if (!validate()) {
    return;
  }

  try {
    await auth.register({ username: username.value, password: password.value });
    toast.add({ severity: 'success', summary: 'Welcome aboard', detail: 'Your account has been created.', life: 3000 });
    router.push({ name: 'feed' });
  } catch (error) {
    formErrors.general = (error as Error).message;
    toast.add({ severity: 'error', summary: 'Sign-up failed', detail: formErrors.general, life: 5000 });
  }
};
</script>

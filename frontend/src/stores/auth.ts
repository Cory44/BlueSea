import { defineStore } from 'pinia';
import { isAxiosError } from 'axios';
import api, { setAuthToken } from '@/services/api';

export interface AuthUser {
  id: number;
  username: string;
  is_admin: boolean;
}

interface AuthState {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

interface AuthResponse {
  user: AuthUser;
  access_token: string;
}

interface Credentials {
  username: string;
  password: string;
}

const STORAGE_KEY = 'bluesea_auth';

function loadPersistedState(): Pick<AuthState, 'user' | 'token'> {
  if (typeof window === 'undefined') {
    return { user: null, token: null };
  }

  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return { user: null, token: null };
  }

  try {
    const parsed = JSON.parse(raw) as Partial<AuthState>;
    return {
      user: parsed.user ?? null,
      token: parsed.token ?? null
    };
  } catch (error) {
    console.warn('Failed to parse persisted auth state', error);
    window.localStorage.removeItem(STORAGE_KEY);
    return { user: null, token: null };
  }
}

function persistState(user: AuthUser | null, token: string | null) {
  if (typeof window === 'undefined') {
    return;
  }

  if (!user || !token) {
    window.localStorage.removeItem(STORAGE_KEY);
    return;
  }

  const payload = JSON.stringify({ user, token });
  window.localStorage.setItem(STORAGE_KEY, payload);
}

function extractErrorMessage(err: unknown): string {
  if (isAxiosError(err)) {
    const response = err.response;
    const message =
      typeof response?.data === 'object' && response?.data !== null && 'message' in response.data
        ? String((response.data as { message: string }).message)
        : null;

    if (message) {
      return message;
    }

    if (response?.status === 401) {
      return 'Invalid username or password.';
    }

    return 'An unexpected error occurred while contacting the server.';
  }

  if (err instanceof Error) {
    return err.message;
  }

  return 'Something went wrong. Please try again later.';
}

const persisted = loadPersistedState();
if (persisted.token) {
  setAuthToken(persisted.token);
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: persisted.user,
    token: persisted.token,
    loading: false,
    error: null
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token)
  },
  actions: {
    async login(credentials: Credentials) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await api.post<AuthResponse>('/auth/login', credentials);
        this.setSession(data.user, data.access_token);
      } catch (error) {
        const message = extractErrorMessage(error);
        this.error = message;
        throw new Error(message);
      } finally {
        this.loading = false;
      }
    },
    async register(credentials: Credentials) {
      this.loading = true;
      this.error = null;

      try {
        const { data } = await api.post<AuthResponse>('/auth/register', credentials);
        this.setSession(data.user, data.access_token);
      } catch (error) {
        const message = extractErrorMessage(error);
        this.error = message;
        throw new Error(message);
      } finally {
        this.loading = false;
      }
    },
    logout() {
      this.setSession(null, null);
    },
    setSession(user: AuthUser | null, token: string | null) {
      this.user = user;
      this.token = token;
      setAuthToken(token);
      persistState(user, token);
    }
  }
});

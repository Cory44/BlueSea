import axios, { AxiosHeaders, type InternalAxiosRequestConfig } from 'axios';

const baseURL = import.meta.env.VITE_API_BASE ?? '/api';

let authToken: string | null = null;

export const setAuthToken = (token: string | null) => {
  authToken = token;
};

export const getAuthToken = () => authToken;

export const api = axios.create({
  baseURL,
  withCredentials: true
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (authToken) {
    const headers = config.headers ?? new AxiosHeaders();
    if (!config.headers) {
      config.headers = headers;
    }
    headers.set('Authorization', `Bearer ${authToken}`);
  }
  return config;
});

export default api;

import { defineStore } from 'pinia';

export const useFeedStore = defineStore('feed', {
  state: () => ({
    refreshToken: 0
  }),
  actions: {
    triggerRefresh() {
      this.refreshToken = Date.now();
    }
  }
});

export type FeedStore = ReturnType<typeof useFeedStore>;

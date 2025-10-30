import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/pages/HomePage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import RegisterPage from '@/pages/RegisterPage.vue';
import FeedPage from '@/pages/FeedPage.vue';
import PostDetailPage from '@/pages/PostDetailPage.vue';
import NewPostPage from '@/pages/NewPostPage.vue';
import { pinia } from '@/stores';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: { requiresGuest: true }
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedPage,
      meta: { requiresAuth: true }
    },
    {
      path: '/posts/new',
      name: 'new-post',
      component: NewPostPage,
      meta: { requiresAuth: true }
    },
    {
      path: '/posts/:id',
      name: 'post',
      component: PostDetailPage,
      meta: { requiresAuth: true }
    }
  ],
  scrollBehavior() {
    return { top: 0 };
  }
});

router.beforeEach((to) => {
  const auth = useAuthStore(pinia);

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return {
      name: 'login',
      query: { redirect: to.fullPath }
    };
  }

  if (to.meta.requiresGuest && auth.isAuthenticated) {
    return { name: 'feed' };
  }

  return true;
});

export default router;

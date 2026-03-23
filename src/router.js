/*
 * router.js
 * Copyright (C) 2023 Christopher Odom <christopher.r.odom@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

// router.js
import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from './components/LandingPage.vue';
import Blog  from './components/BlogIndex.vue';
import BlogViewer from './blog/BlogViewer.vue';
import ResumeView from './components/ResumeView.vue';

export const routes = [
    {
        path: '/',
        component: LandingPage,
    },
    {
        path: '/blog',
        component: Blog,
    },
    {
        path: '/blog/:id',
        component: BlogViewer,
    },
    {
        path: '/resume',
        component: ResumeView,
    }
]
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

/*
 * router.js
 * Copyright (C) 2023 Christopher Odom <christopher.r.odom@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

// router.js
import { createRouter, createWebHistory } from 'vue-router';
import About from './components/TheWelcome.vue';
import Blog  from './components/BlogIndex.vue';
import BlogViewer from './blog/BlogViewer.vue';
import ResumeView from './components/ResumeView.vue';
import { animateRouteChange } from './assets/animations.js';

const routes = [
    {
        path: '/',
        component: About,
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

router.afterEach((to, from) => {
  animateRouteChange(to, from);
});

export default router;

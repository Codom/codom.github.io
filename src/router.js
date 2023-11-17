/*
 * router.js
 * Copyright (C) 2023 Christopher Odom <christopher.r.odom@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

import { createRouter, createWebHistory } from 'vue-router';
import About from './components/TheWelcome.vue';
import Blog  from './components/BlogIndex.vue';
import StaticWebsite from './blog/static_website.vue';
import VuePort from './blog/vue_port.vue';

import BlogViewer from './blog/BlogViewer.vue'

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
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;

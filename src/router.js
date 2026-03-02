/*
 * router.js
 * Copyright (C) 2023 Christopher Odom <christopher.r.odom@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

// router.js
import About from './components/TheWelcome.vue';
import Blog  from './components/BlogIndex.vue';
import BlogViewer from './blog/BlogViewer.vue';
import ResumeView from './components/ResumeView.vue';

export const routes = [
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

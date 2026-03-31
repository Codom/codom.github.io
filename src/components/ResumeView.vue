<template>
    <div class="page-wrapper">
        <div class="paper-card">
            <div v-html="resumeHtml" class="markdown-body"></div>
        </div>
    </div>
</template>

<script>
import resumeHtml from '../data/resume.html?raw'

export default {
    setup() {
        return {
            resumeHtml
        }
    }
}
</script>

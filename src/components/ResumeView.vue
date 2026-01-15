<template>
    <div class="page-wrapper">
        <div v-if="loading" class="loading">Loading resume...</div>
        <div v-if="error" class="error">{{ error }}</div>
        
        <div v-if="resumeHtml" class="paper-card">
            <div v-html="resumeHtml" class="markdown-body"></div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            loading: true,
            error: null,
            resumeHtml: null
        }
    },
    mounted() {
        fetch('/resume.html')
            .then(async response => {
                if (!response.ok) {
                    throw new Error(`Failed to load resume: ${response.statusText}`);
                }
                this.resumeHtml = await response.text();
                this.loading = false;
            })
            .catch(err => {
                this.error = err.message;
                this.loading = false;
            });
    }
}
</script>

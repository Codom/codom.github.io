<template>
    <div class="resume-container">
        <embed src="/resume.pdf" type="application/pdf" width="100%" height="800px" />
        <p class="fallback">
            Unable to display PDF file. <a href="/resume.pdf" download>Download</a> instead.
        </p>
    </div>
</template>

<style scoped>
.resume-container {
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}
.fallback {
    text-align: center;
    margin-top: 10px;
}
</style>

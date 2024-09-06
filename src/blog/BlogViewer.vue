<template>
    <div class="post">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-if="error" class="error">{{ error }}</div>

        <div v-if="post" class="content">
            <div v-html="post" class="content"></div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            loading: false,
            post: null,
            error: null,
        }
    },    // watch the params of the route to fetch the data again
    created() {
        this.$watch(
          () => this.$route.params,
          () => {
            this.fetchData()
          },
          // fetch the data when the view is created and the data is
          // already being observed
          { immediate: true }
        )
    },
    methods: {
        fetchData() {
          this.error = this.post = null
          this.loading = true
          const data_uri = this.$route.params.id + '.html'
          fetch(data_uri).then(async (response) => {
            this.loading = false
            if (!response.ok) {
              this.error = await response.error()
            } else {
              const html_text = await response.text()
              this.post = html_text
            }
          })
        },
    },
}
</script>
<style>
</style>

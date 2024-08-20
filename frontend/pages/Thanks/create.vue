<template>
  <div>
    <h2>Create New Post</h2>
    <form @submit.prevent="createPost">
      <input v-model="newPost.title" placeholder="Title" />
      <textarea v-model="newPost.content" placeholder="Content"></textarea>
      <input type="file" @change="onFileChange" />
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  data() {
    return {
      newPost: {
        title: '',
        content: '',
        image: null
      }
    }
  },
  methods: {
    onFileChange(e) {
      this.newPost.image = e.target.files[0]
    },
    async createPost() {
      const formData = new FormData()
      formData.append('title', this.newPost.title)
      formData.append('content', this.newPost.content)
      if (this.newPost.image) {
        formData.append('image', this.newPost.image)
      }

      await fetch('http://localhost:5000/posts', {
        method: 'POST',
        body: formData
      })

      this.newPost.title = ''
      this.newPost.content = ''
      this.newPost.image = null
    }
  }
}
</script>
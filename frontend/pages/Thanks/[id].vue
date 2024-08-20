<template>
  <Content>
    <div v-if="loading">
      <p>Loading...</p>
    </div>
    <div v-else-if="image">
      {{ image }}
      <img :src="image.main_image_path" alt="">
      <img :src="sub" alt="" v-for="sub in image.sub_image_paths" :key="sub">
      {{ image.author_name }}
      <p v-if="image.comments">{{ image.comments }}</p>
      <ul v-if="image.tags">
        <li v-for="tag in image.tags" :key="tag">{{ tag }}</li>
      </ul>
    </div>
    <div v-else>
      <p>Image not found.</p>
    </div>
  </Content>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Content from "~/components/app/Content.vue";

interface ImageData {
  id: number
  author_name: string
  main_image_path: string
  sub_image_paths: string[]
  tags: string[]
  comments: string
}

const route = useRoute()
const image = ref<ImageData | null>(null)
const loading = ref(true)  // ローディング状態を管理するための変数

onMounted(async () => {
  try {
    const response = await fetch(`/api/images/${route.params.id}`)
    if (response.ok) {
      image.value = await response.json() as ImageData
      console.log(image)
    } else {
      console.error('Failed to fetch image')
    }
  } catch (error) {
    console.error('An error occurred while fetching the image:', error)
  } finally {
    loading.value = false  // データ取得が完了したらローディングを終了
  }
})
</script>

<style lang="scss" scoped>
div {
  background-image: url("@/assets/img/paper.jpg");
  border-radius: 2px;
}
</style>
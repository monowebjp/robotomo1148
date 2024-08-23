<template>
  <Content bg-type="paper">
    <div v-if="loading">
      <p>Loading...</p>
    </div>
    <div v-else-if="image">
      <PrevButton to-path="/thanks">一覧に戻る</PrevButton>
      <ImageSlides :main-path="image.main_image_path" :sub-paths="image.sub_image_paths" />
      <dl>
        <dt><i class="c-icon c-icon--user"></i></dt>
        <dd>{{ image.author_name }} 様</dd>
      </dl>
      <dl>
        <dt><i class="c-icon c-icon--priceTag"></i></dt>
        <dd>
          <Tags :tags="image.tags" />
        </dd>
      </dl>

      <div class="c-box">
        <p v-if="image.comments">{{ image.comments }}</p>
      </div>

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
import Tags from "~/components/atoms/Tags.vue";
import ImageSlides from "~/components/molecules/ImageSlides.vue";
import PrevButton from "~/components/atoms/PrevButton.vue";

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
dl {
  display: flex;

  + dl {
    margin-top: 10px;
  }
}

dt {
  margin-right: 5px;
}

.c-box {
  margin-top: 30px;
  padding: 20px;
  background: $bg-color-1;
  border-radius: 4px;
}
</style>
<template>
  <Content>
    <div class="message">
      <p>いただいたもの（依頼含む）、時期などごちゃまぜで掲載しています<br>全部ありがとう！宝物です！</p>
      <p class="u-fsS">※ データを飛ばした時期があるので掲載できていないものもあります、本当にごめんなさい！</p>
    </div>
    <Search />
    <ImageGallery :images="images" />
    <div v-if="hasMore">
      <button @click="nextPage">次へ</button>
    </div>
  </Content>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Search from "~/components/molecules/Search.vue";
import ImageGallery from "~/components/molecules/ImageGallery.vue";
import Content from "~/components/app/Content.vue";

interface Image {
  id: number
  main_image_path: string
}

const images = ref<Image[]>([])
const page = ref(1)  // 現在のページ
const hasMore = ref(true)  // 次のページがあるかどうかを管理

// データをロードする関数
const loadImages = async () => {
  try {
    const response = await fetch(`/api/images?page=${page.value}&limit=30`)
    if (response.ok) {
      const data = await response.json()
      images.value.push(...data.images)  // 取得した画像を追加
      hasMore.value = data.pages > page.value  // 次のページがあるかどうか確認
    } else {
      console.error('Failed to fetch images')
    }
  } catch (error) {
    console.error('An error occurred while fetching the images:', error)
  }
}

onMounted(async () => {
  await loadImages()
})

// 次のページを取得する関数
const nextPage = async () => {
  page.value += 1  // ページ番号を増やす
  await loadImages()
}
</script>

<style lang="scss" scoped>
.message {
  position: relative;
  box-sizing: border-box;
  padding: 40px 70px;
  color: $font-color;
  &::before {
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
    content: "";
    width: 100%;
    height: 100%;
    background-image: url("@/assets/img/paper.jpg");
    background-size: cover;
    opacity: .955;
    border-radius: 4px;
  }
}

p + p {
  margin-top: 15px;
}

.u-fsS {
  font-size: 13px;
}
</style>
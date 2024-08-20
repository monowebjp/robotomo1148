<template>
  <Content>
    <div class="message">
      <p>いただいたもの（依頼含む）、時期などごちゃまぜで掲載しています<br>全部ありがとう！宝物です！</p>
      <p class="u-fsS">※ データを飛ばした時期があるので掲載できていないものもあります、本当にごめんなさい！</p>
    </div>
    <Search />
    <ImageGallery :images="images" />
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

onMounted(async () => {
  const response = await fetch('/api/images')
  if (response.ok) {
    images.value = await response.json() as Image[]
  } else {
    console.error('Failed to fetch images')
  }
})
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
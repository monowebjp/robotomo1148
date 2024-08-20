<template>
  <div class="m-imageGallery">
    <div class="m-imageGallery__item" v-for="image in images" :key="image.id">
      <nuxt-link :to="'/thanks/' + image.id">
        <img :src="image.main_image_path" alt="" loading="lazy">
      </nuxt-link>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    images: {
      type: {
        id: Number,
        main_image_path: String
      }<Array>,
      required: true
    }
  }
}
</script>

<style lang="scss" scoped>
.m-imageGallery {
  column-count: 3;

  &__item {
    break-inside: avoid;
    margin: 0 0 15px;
    background: $white;
    border-radius: 2px;
  }
}

a {
  display: block;
  padding: 50px;

  &:hover {
    img {
      opacity: .8;
      transform: scale(1);
    }
  }
}

img {
  margin: 0 auto;
  max-width: 100%;
  height: auto;
  transform: scale(.95);
  transition: opacity .15s ease-out, transform .2s ease-out;
}
</style>
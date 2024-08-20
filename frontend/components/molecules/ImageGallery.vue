<template>
  <div class="m-imageGallery">
    <div class="m-imageGallery__item" v-for="item in items" :key="item.src">
      <nuxt-link :to="'/thanks/1'">
        <img :src="'/img/thanks/' + item.src" alt="" loading="lazy">
      </nuxt-link>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    items: {
      type: {
        src: String
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
    }
  }
}

img {
  margin: 0 auto;
  max-width: 100%;
  height: auto;
  transition: opacity .15s ease-out;
}
</style>
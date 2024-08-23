<template>
  <button>
    <nuxt-link :to="toPath">
      <i class="c-icon c-icon--prev"></i>
      <span><slot /></span>
    </nuxt-link>
  </button>
</template>
<script lang="ts">
export default {
  props: {
    toPath: {
      type: String,
      required: true
    }
  }
}
</script>
<style lang="scss">
button {
  border: 0;

  &:hover {
    cursor: pointer;
  }
}

a {
  text-decoration: none;
  color: $font-color;
}

.c-icon {
  margin-right: 5px;
}
</style>
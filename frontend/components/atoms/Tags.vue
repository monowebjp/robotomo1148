<template>
  <ul>
    <li v-for="tag in tags" :key="tag">{{ tag }}</li>
  </ul>
</template>

<script lang="ts">
export default {
  props: {
    tags: {
      type: String<Array>,
      required: true
    }
  }
}
</script>

<style lang="scss" scoped>
ul, li {
  margin: 0;
  padding: 0;
}

ul {
  display: flex;
}

li {
  padding: 2px 12px;
  border-radius: 15px;
  list-style: none;
  font-size: 1.2rem;
  background: $sub-color-1;
  color: $white;
  font-weight: 700;
  letter-spacing: -.3px;

  + li {
    margin-left: 5px;
  }
}
</style>
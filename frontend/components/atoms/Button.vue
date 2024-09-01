<template>
  <button :type="type"><slot /></button>
</template>
<script lang="ts">
export default {
  props: {
    type: {
      type: String
    }
  }
}
</script>

<style lang="scss" scoped>
button {
  border: 0;
  background: $primary-color;
  color: $white;
  font-weight: 700;
  padding: 8px 15px;
  border-radius: 2px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, .3);
  transition: box-shadow .15s ease-out;

  &:hover {
    cursor: pointer;
    box-shadow: 4px 4px 10px rgba(0, 0, 0, .4);
  }
}
</style>
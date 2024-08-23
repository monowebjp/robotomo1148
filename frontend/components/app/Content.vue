<template>
  <div style="width: 55%; overflow-y: scroll; padding-bottom: 300px;">
    <div :class="{ paper: bgType === 'paper' }">
      <slot />
    </div>
  </div>
</template>
<script lang="ts">
export default {
  props: {
    bgType: {
      type: String,
      default: null // 任意: 初期値を設定する場合
    }
  }
}
</script>
<style lang="scss">
.paper {
  background-image: url("@/assets/img/paper.jpg");
  border-radius: 2px;
  padding: 20px;
}
</style>
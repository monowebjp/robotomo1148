<template>
  <div>
    <input type="search" placeholder="キーワードを入力してください">
    <Button>絞り込む</Button>
  </div>
</template>

<style lang="scss" scoped>
div {
  padding: 50px 0;
  text-align: center;
}

input {
  margin-right: 5px;
  padding: 8px 15px;
  width: 30vw;
  border-radius: 2px;
  border: 0;
  color: $font-color;
  background: $white;

}
</style>
<script setup lang="ts">
import Button from "~/components/atoms/Button.vue";
</script>
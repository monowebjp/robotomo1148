<template>
  <header>
    <h1>ROBOTOMO1148</h1>
    <GlobalNav />
  </header>
</template>

<script setup lang="ts">
import GlobalNav from "~/components/app/GlobalNav.vue";
</script>

<style lang="scss" scoped>
header {
  margin: 25px 0 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  letter-spacing: 3px;
  color: $white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, .7), -1px -1px 2px rgba(0, 0, 0, .5)；
}
</style>
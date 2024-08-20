<template>
  <div class="l-container">
    <Header />
    <div class="l-content">
      <NuxtPage />
    </div>
    <div class="p-character">
      <div class="p-character__chair" />
      <div class="p-character__desk" />
    </div>
  </div>
</template>
<script setup lang="ts">
import Header from "~/components/app/Header.vue";
</script>

<style lang="scss" scoped>
.l-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  box-sizing: border-box;
  padding: 0 22px;
  background-image: url("@/assets/img/room.png");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.l-content {
  display: flex;
  justify-content: end;
  height: calc(100vh - 35px);
  width: 100%;
}

.p-character {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  pointer-events: none;

  &__desk,
  &__chair {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: 0 bottom;
  }

  &__desk {
    background-image: url("@/assets/img/desk.png");
    aspect-ratio: 2000 / 269;
  }

  &__chair {
    background-image: url("@/assets/img/chair.png");
    aspect-ratio: 2000 / 626;
  }
}
</style>
<template>
  <Content>
    <div class="message">
      <p>いただいたもの（依頼含む）、時期などごちゃまぜで掲載しています<br>全部ありがとう！宝物です！</p>
      <p class="u-fsS">※ データを飛ばした時期があるので掲載できていないものもあります、本当にごめんなさい！</p>
    </div>
    <Search />
    <ImageGallery :items="imageGalleryItems" />
  </Content>
</template>

<script setup lang="ts">
import Search from "~/components/molecules/Search.vue";
import ImageGallery from "~/components/molecules/ImageGallery.vue";
import Content from "~/components/app/Content.vue";

const imageGalleryItems = [{src: "230628motyo-1934.png"},{src: "230830motyo-2302.png"},{src: "231017motyo-2719.png"},{src: "231029motyo-2823.png"},{src: "231107motyo-2886.png"},{src: "231123motyo-3000.png"},{src: "231129motyo-3054.png"},{src: "231220motyo-3242.png"},{src: "240131motyo-3557.png"},{src: "240131motyo-3571.png"},{src: "240207motyo-3588.png"},{src: "240313motyo-3879.png"},{src: "240315motyo-3903.png"},{src: "240409motyo-4127.png"},{src: "240507motyo-4358.png"},{src: "240626motyo-4751.png"},{src: "240721motyo-4944.png"},{src: "240815motyo-5069.png"},{src: "24NY-motyo027.png"},{src: "amongus.png"},{src: "bibibibi.png"},{src: "bokujou-monogatari.jpg"},{src: "capybara-dash.gif"},{src: "dgmon.gif"},{src: "futaba-hajime.jpg"},{src: "game-playing.png"},{src: "gz-logo.png"},{src: "hirune.png"},{src: "jet-coaster.png"},{src: "kitune-01.png"},{src: "kitune-10.png"},{src: "kitune-ds.png"},{src: "kitune-ds1.png"},{src: "kitune-ds2.png"},{src: "kitune-helloween.png"},{src: "kitune-oinori.png"},{src: "kitune-santa.png"},{src: "kitune-unchi.png"},{src: "mini-robo-01.png"},{src: "mini-robo-02.png"},{src: "mini-robo-03.png"},{src: "monhan.png"},{src: "refine-the-self.gif"},{src: "tsumutama-01.jpg"},{src: "yurukimono-01.jpg"}]

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
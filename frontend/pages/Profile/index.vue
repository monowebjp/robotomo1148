<template>
  <Content>
    <div>
      <h2>ロボトモ3面図</h2>
      <img src="/img/profile/setting.jpg" style="width: 500px;" />
      <h2>配信アーカイブリスト</h2>
      <ul>
        <li>ダークソウル REMASTERED</li>
        <li>ダークソウル 2 SKULER OF FIRST SIN</li>
        <li>ダークソウル 3 </li>
        <li>ドットホラーストーリー</li>
        <li>ドットホラーストーリー 2</li>
        <li>HOTEL SOULS</li>
        <li>モンスターハンター ワールド アイスボーン</li>
        <li>パラノマサイト</li>
        <li>8番出口</li>
        <li>偽夢</li>
        <li>8番のりば</li>
        <li>ファズモフォビア</li>
        <li>クロノクロス</li>
        <li>クロノトリガー</li>
        <li>アーマードコア6</li>
        <li>SEKIRO</li>
        <li>OUTER WILDS</li>
        <li>VA-11-HA-LA</li>
        <li>ELDEN RING</li>
      </ul>
    </div>
  </Content>
</template>

<script setup lang="ts">
import Content from "~/components/app/Content.vue";
</script>

<style lang="scss" scoped>
div {
  padding: 15px 20px;
  background-image: url("@/assets/img/paper.jpg");
  border-radius: 2px;
}

h2 {
  position: relative;
  text-align: center;
  margin: 80px 0 30px;
  padding: 0 0 25px;
  letter-spacing: .5px;

  &::after {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    content: "";
    display: block;
    height: 2px;
    width: 80px;
    background: $primary-color;
  }

  &:first-child {
    margin-top: 0;
  }
}

img {
  margin: 0 auto;
  max-width: 100%;
  height: auto;
}
</style>
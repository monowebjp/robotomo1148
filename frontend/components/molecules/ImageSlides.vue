<template>
  <div>
    <div class="main" :class="{'u-bg--Dark': currentImageHasBackground}">
      <img :src="mainSlide" alt="" class="main__img">
    </div>
    <ul v-if="subPaths.length > 0">
      <li>
        <input id="imageSlide0" type="radio" v-model="mainSlide" :value="mainPath">
        <label for="imageSlide0">
          <img :src="mainPath" alt="">
        </label>
      </li>
      <li v-for="(subPath, index) in subPaths" :key="subPath">
        <input :id="`'imageSlide${index+1}`" type="radio" v-model="mainSlide" :value="subPath.filename">
        <label :for="`'imageSlide${index+1}`" :class="{'u-bg--Dark': subPath.has_background}">
          <img :src="subPath.filename" alt="">
        </label>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    mainPath: {
      type: String,
      required: true
    },
    mainBg: {
      type: Boolean,
      required: true
    },
    subPaths: {
      type: Array
    }
  },
  data() {
    return {
      mainSlide: this.mainPath,
      currentImageHasBackground: this.mainBg
    }
  },
  watch: {
    mainSlide(newSlide) {
      this.updateBackgroundStatus(newSlide);
    }
  },
  mounted() {
    this.updateBackgroundStatus(this.mainSlide);
  },
  methods: {
    updateBackgroundStatus(slide) {
      if (slide === this.mainPath) {
        this.currentImageHasBackground = this.mainBg; // メイン画像には背景色がない前提（必要に応じて変更）
      } else {
        const selectedSubPath = this.subPaths.find(subPath => subPath.filename === slide);
        this.currentImageHasBackground = selectedSubPath ? selectedSubPath.has_background : false;
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  margin-top: 20px;
  padding: 20px;

  &__img {
    margin: 0 auto;
    max-width: 100%;
  }
}

ul, li {
  margin: 0;
  padding: 0;
}

ul {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

li {
  margin: 0 3px;
  list-style: none;
  max-width: 80px;
  border: 2px solid $sub-color-1;
  border-radius: 2px;
}

input:checked + label {
  background: $sub-color-1;

  > img {
    transform: scale(1);
    opacity: 1;
  }

  &:hover {
    > img {
      cursor: default;
    }
  }
}

label {
  display: block;
  padding: 5px;

  > img {
    transform: scale(.9);
    transition: opacity .15s ease-out, transform .15s ease-out;
  }

  &:hover {
    cursor: pointer;
    > img {
      transform: scale(1);
      opacity: .75;
    }
  }
}

.u-bg--Dark {
  background: $mono-color-400;
}

input {
  display: none;
}
</style>
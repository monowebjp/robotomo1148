<template>
  <div>
    <img :src="mainSlide" alt="" class="main">
    <ul v-if="subPaths.length > 0">
      <li>
        <input id="imageSlide0" type="radio" v-model="mainSlide" :value="mainPath">
        <label for="imageSlide0">
          <img :src="mainPath" alt="">
        </label>
      </li>
      <li v-for="(subPath, index) in subPaths" :key="subPath">
        <input :id="`'imageSlide${index+1}`" type="radio" v-model="mainSlide" :value="subPath">
        <label :for="`'imageSlide${index+1}`">
          <img :src="subPath" alt="">
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
    subPaths: {
      type: Array
    }
  },
  data() {
    return {
      mainSlide: this.mainPath
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  margin: 0 auto;
  max-width: 100%;
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

input {
  display: none;
}
</style>
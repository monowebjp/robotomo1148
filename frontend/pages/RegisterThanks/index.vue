<template>
  <Content bg-type="paper">
    <h1>いただいた画像登録</h1>
    <form @submit.prevent="registerImage" enctype="multipart/form-data">
      <dl>
        <dt><label for="author_name">書いてくれた人</label></dt>
        <dd><input v-model="form.author_name" id="author_name" required /></dd>
      </dl>
      <dl>
        <dt><label for="main_image">メイン画像</label></dt>
        <dd><input type="file" @change="handleMainImage" id="main_image" required /></dd>
        <dd>
          <input type="checkbox" v-model="form.main_image_has_background" id="main_image_has_background" />
          <label for="main_image_has_background">背景色を持つか</label>
        </dd>
      </dl>
      <dl>
        <dt><label for="sub_images">サブ画像 (5枚まで)</label></dt>
        <dd><input type="file" @change="handleSubImages" id="sub_images" multiple /></dd>
      </dl>
      <dl v-for="(image, index) in form.sub_images" :key="index">
        <dt>
          <label :for="`sub_image_has_background_${index}`">背景色を持つか ({{ image.file.name }})</label>
        </dt>
        <dd>
          <input type="checkbox" v-model="image.hasBackground" :id="`sub_image_has_background_${index}`" />
        </dd>
      </dl>
      <dl>
        <dt><label for="tags">タグ (カンマで分割)</label></dt>
        <dd><input v-model="form.tags" id="tags" /></dd>
      </dl>
      <dl>
        <dt><label for="comments">コメント</label></dt>
        <dd><textarea v-model="form.comments" id="comments"></textarea></dd>
      </dl>
      <Button type="submit">保存</Button>
    </form>
  </Content>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Content from "~/components/app/Content.vue";
import Button from "~/components/atoms/Button.vue";

interface SubImage {
  file: File
  hasBackground: boolean
}

interface Form {
  author_name: string
  main_image: File | null
  main_image_has_background: boolean
  sub_images: SubImage[]
  tags: string
  comments: string
}

const form = ref<Form>({
  author_name: '',
  main_image: null,
  main_image_has_background: false,
  sub_images: [],
  tags: '',
  comments: ''
})

const handleMainImage = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    form.value.main_image = target.files[0]
  }
}

const handleSubImages = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    form.value.sub_images = Array.from(target.files).slice(0, 5).map(file => ({
      file,
      hasBackground: false
    }))
  }
}

const registerImage = async () => {
  const formData = new FormData()
  formData.append('author_name', form.value.author_name)
  if (form.value.main_image) {
    formData.append('main_image', form.value.main_image)
  }
  formData.append('main_image_has_background', form.value.main_image_has_background.toString())
  form.value.sub_images.forEach((image, index) => {
    formData.append('sub_images', image.file)
    formData.append(`sub_image_has_background_${index}`, image.hasBackground.toString())
  })
  formData.append('tags', form.value.tags.split(',').map(tag => tag.trim()).join(','))
  formData.append('comments', form.value.comments)

  try {
    const response = await fetch('/api/images', {
      method: 'POST',
      body: formData,
    })

    if (response.ok) {
      alert('Image registered successfully')
    } else {
      alert(`Error: ${response.status}`)
    }
  } catch (error) {
    console.error('Error:', error)
    alert('An error occurred during registration')
  }
}
</script>
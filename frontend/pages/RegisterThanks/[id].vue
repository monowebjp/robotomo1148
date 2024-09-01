<template>
  <Content bg-type="paper">
    <div>
      <h1>画像登録修正</h1>
      <form @submit.prevent="submitForm">
        <dl>
          <dt><label for="author_name">書いてくれた人</label></dt>
          <dd><input v-model="formData.author_name" id="author_name" type="text" required /></dd>
        </dl>
        <dl>
          <dt>メイン画像</dt>
          <dd><input id="main_image" type="file" @change="handleMainImageUpload" /></dd>
          <dd>
            <input v-model="formData.main_image_has_background" id="main_image_has_background" type="checkbox" />
            <label for="main_image_has_background">背景色を持つか</label>
          </dd>
        </dl>
        <dl>
          <dt><label for="sub_images">サブ画像 (5枚まで)</label></dt>
          <dd> <input id="sub_images" type="file" multiple @change="handleSubImagesUpload" /></dd>
        </dl>
        <dl v-for="(subImage, index) in formData.sub_images" :key="index">
          <dt>
            <label :for="'sub_image_has_background_' + index">背景色を持つか</label>
          </dt>
          <dd>
            <input v-model="subImage.has_background" :id="'sub_image_has_background_' + index" type="checkbox" />
          </dd>
        </dl>
        <dl>
          <dt><label for="tags">タグ (カンマで分割)</label></dt>
          <dd><input v-model="formData.tags" id="tags" type="text" placeholder="Comma separated tags" /></dd>
        </dl>
        <dl>
          <dt><label for="comments">コメント</label></dt>
          <dd><textarea v-model="formData.comments" id="comments"></textarea></dd>
        </dl>
        <Button type="submit">保存</Button>
      </form>
    </div>
  </Content>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Content from "~/components/app/Content.vue";
import Button from "~/components/atoms/Button.vue";

interface SubImage {
  file: File | null
  has_background: boolean
}

interface FormData {
  author_name: string
  main_image: File | null
  main_image_has_background: boolean
  sub_images: SubImage[]
  tags: string
  comments: string
}

const router = useRouter()
const route = useRoute()

const formData = ref<FormData>({
  author_name: '',
  main_image: null,
  main_image_has_background: false,
  sub_images: [],
  tags: '',
  comments: ''
})

const handleMainImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    formData.value.main_image = target.files[0]
  }
}

const handleSubImagesUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  formData.value.sub_images = []
  if (target.files) {
    for (let i = 0; i < target.files.length; i++) {
      formData.value.sub_images.push({
        file: target.files[i],
        has_background: false
      })
    }
  }
}

const loadImageData = async () => {
  try {
    const response = await fetch(`/api/images/${route.params.id}`)
    if (!response.ok) {
      throw new Error('Failed to fetch image data')
    }
    const data = await response.json()
    formData.value.author_name = data.author_name
    formData.value.main_image_has_background = data.main_image_has_background
    formData.value.sub_images = data.sub_image_paths.map((subImage: any) => ({
      file: null,
      has_background: subImage.has_background
    }))
    formData.value.tags = data.tags.join(',')
    formData.value.comments = data.comments
  } catch (error) {
    console.error('Error loading image data:', error)
  }
}

const submitForm = async () => {
  const formDataToSubmit = new FormData()
  formDataToSubmit.append('author_name', formData.value.author_name)
  formDataToSubmit.append('main_image_has_background', formData.value.main_image_has_background.toString())

  if (formData.value.main_image) {
    formDataToSubmit.append('main_image', formData.value.main_image)
  }

  formData.value.sub_images.forEach((subImage, index) => {
    if (subImage.file) {
      formDataToSubmit.append('sub_images', subImage.file)
      formDataToSubmit.append(`sub_image_has_background_${index}`, subImage.has_background.toString())
    }
  })

  formDataToSubmit.append('tags', formData.value.tags)
  formDataToSubmit.append('comments', formData.value.comments)

  try {
    const response = await fetch(`/api/images/${route.params.id}`, {
      method: 'PUT',
      body: formDataToSubmit,
    })

    if (!response.ok) {
      throw new Error('Failed to update image')
    }

    alert('Image updated successfully!')
    router.push('/')
  } catch (error) {
    console.error('Error updating image:', error)
  }
}

onMounted(loadImageData)
</script>
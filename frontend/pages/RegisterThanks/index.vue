<template>
  <Content bg-type="paper">
    <h1>いただいた画像登録</h1>
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
      <dl>
        <dt><label for="author_name">書いてくれた人</label></dt>
        <select v-model="form.author_id" @change="handleAuthorChange">
          <option value="">著者を選択</option>
          <option v-for="author in authors" :key="author.id" :value="author.id">
            {{ author.author_name }}
          </option>
          <!-- 新規登録用のオプション -->
          <option value="new">新規登録</option>
        </select>
      </dl>

      <!-- 新規著者名の入力フォーム（新規登録が選択された場合に表示） -->
      <div v-if="form.author_id === 'new'">
        <label for="new_author_name">新規著者名:</label>
        <input type="text" v-model="form.new_author_name" placeholder="新しい著者名を入力" required />

        <!-- SNS URLを動的に入力できるフォーム -->
        <div>
          <label for="new_author_sns">SNS URL:</label>
          <div v-for="(sns, index) in form.new_author_sns_urls" :key="index">
            <input type="text" v-model="form.new_author_sns_urls[index]" placeholder="SNS URLを入力" />
            <button type="button" @click="removeSnsUrl(index)">削除</button>
          </div>
          <button type="button" @click="addSnsUrl">SNS URLを追加</button>
        </div>
      </div>

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
import { ref, reactive } from 'vue'
import Content from "~/components/app/Content.vue";
import Button from "~/components/atoms/Button.vue";

interface SubImage {
  file: File
  hasBackground: boolean
}

interface Form {
  author_id: string
  new_author_name: string
  new_author_sns_urls: string[]
  main_image: File | null
  main_image_has_background: boolean
  sub_images: SubImage[]
  tags: string
  comments: string
}

const form = reactive<Form>({
  author_id: '',              // 既存著者のID
  new_author_name: '',         // 新規著者名
  new_author_sns_urls: [''],   // 新規著者のSNS URL配列
  main_image: null,
  main_image_has_background: false,
  sub_images: [],
  tags: '',
  comments: ''
})

const authors = ref([]); // 著者リストを取得して格納

// 著者選択の変更イベント
const handleAuthorChange = () => {
  if (form.author_id === 'new') {
    form.new_author_name = ''
    form.new_author_sns_urls = ['']
  }
}

const handleMainImage = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    form.main_image = target.files[0]
  }
}

// サブ画像の処理
const handleSubImages = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    form.sub_images = Array.from(target.files).slice(0, 5).map(file => ({
      file,
      hasBackground: false
    }))
  }
}

// SNS URLの追加・削除
const addSnsUrl = () => form.new_author_sns_urls.push('');
const removeSnsUrl = (index: number) => form.new_author_sns_urls.splice(index, 1);

// 画像登録処理
const submitForm = async () => {
  const formData = new FormData();

  // 著者IDか新規著者情報を送信
  if (form.author_id === 'new') {
    formData.append('new_author_name', form.new_author_name);
    form.new_author_sns_urls.forEach((url, index) => {
      formData.append(`new_author_sns_urls[${index}]`, url);
    });
  } else {
    formData.append('author_id', form.author_id || '');
  }

  // メイン画像の追加
  if (form.main_image) {
    formData.append('main_image', form.main_image);
  }
  formData.append('main_image_has_background', form.main_image_has_background.toString());

  // サブ画像の追加
  form.sub_images.forEach((image, index) => {
    formData.append('sub_images', image.file);
    formData.append(`sub_image_has_background_${index}`, image.hasBackground.toString());
  });

  // タグとコメントの追加
  formData.append('tags', form.tags.split(',').map(tag => tag.trim()).join(','));
  formData.append('comments', form.comments);

  try {
    const response = await fetch('/api/images', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      alert('画像が正常に登録されました');
    } else {
      alert(`エラー: ${response.status}`);
    }
  } catch (error) {
    console.error('登録中にエラーが発生しました:', error);
    alert('登録中にエラーが発生しました');
  }
};

// 著者リストを取得
const fetchAuthors = async () => {
  try {
    const response = await fetch('/api/authors');
    if (!response.ok) {
      throw new Error('著者リストの取得ぺろぺろ');
    }
    authors.value = await response.json();
  } catch (error) {
    console.error('著者リストの取得エラー:', error);
    alert(`著者リストの取得に失敗しました: ${error.message}`);
  }
};

// コンポーネントがマウントされた時に著者リストを取得
fetchAuthors();
</script>

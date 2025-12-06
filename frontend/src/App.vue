<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import FileUploader from './components/FileUploader.vue'
import FileList from './components/FileList.vue'
import SummaryResult from './components/SummaryResult.vue'

const files = ref([])
const isProcessing = ref(false)
const result = ref(null)

const handleFilesSelected = (newFiles) => {
  files.value = [...files.value, ...newFiles]
  // Hide previous result if adding new files
  if (result.value) {
    result.value = null
  }
}

const handleRemoveFile = (index) => {
  files.value.splice(index, 1)
}

const handleReset = () => {
  files.value = []
  result.value = null
}

const handleSubmit = async () => {
  if (files.value.length === 0) return

  isProcessing.value = true
  result.value = null

  const formData = new FormData()
  files.value.forEach(file => {
    formData.append('files', file)
  })

  try {
    const response = await axios.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data.error) {
      throw new Error(response.data.message)
    }

    result.value = response.data
  } catch (error) {
    console.error('Error:', error)
    alert(`上傳發生錯誤: ${error.message || '未知錯誤'}`)
  } finally {
    isProcessing.value = false
  }
}

const buttonText = computed(() => {
  if (isProcessing.value) return '處理中...'
  return '上傳並分析'
})
</script>

<template>
  <div class="wrapper">
    <div class="card">
      <h1>AI 筆記摘要助手</h1>
      <p class="subtitle">
        上傳 PDF 或 PPT 投影片，AI 將自動為您生成重點摘要並同步至 Notion。
      </p>

      <form @submit.prevent="handleSubmit">
        <FileUploader @files-selected="handleFilesSelected" />

        <FileList :files="files" @remove-file="handleRemoveFile" />

        <div class="button-group">
          <button 
            type="button" 
            v-if="files.length > 0" 
            class="secondary-btn" 
            @click="handleReset"
            :disabled="isProcessing"
          >
            重新選擇
          </button>
          
          <button 
            type="submit" 
            :disabled="files.length === 0 || isProcessing"
          >
            {{ buttonText }}
          </button>
        </div>
      </form>

      <SummaryResult v-if="result" :result="result" />
    </div>
  </div>
</template>

<style>
/* Global Styles from original CSS */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    background: #f3f4f6;
}

.wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
}

.card {
    background: #ffffff;
    padding: 32px 40px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
    max-width: 800px;
    width: 100%;
}

h1 {
    margin: 0 0 4px;
    font-size: 28px;
}

.subtitle {
    margin: 0 0 24px;
    font-size: 14px;
    color: #6b7280;
}

.button-group {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

button {
    width: 100%;
    padding: 14px 24px;
    border-radius: 12px;
    border: none;
    font-size: 16px;
    cursor: pointer;
    background: #4f46e5;
    color: #ffffff;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
    transition: background 0.2s;
    display: block;
    flex: 1;
}

button:hover {
    background: #4338ca;
}

button:disabled {
    background: #a5b4fc;
    cursor: not-allowed;
    box-shadow: none;
}

.secondary-btn {
    background: #e5e7eb;
    color: #374151;
    box-shadow: none;
}

.secondary-btn:hover {
    background: #d1d5db;
}
</style>

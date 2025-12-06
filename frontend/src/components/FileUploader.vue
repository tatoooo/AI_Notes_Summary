<script setup>
import { ref } from 'vue'

const emit = defineEmits(['files-selected'])
const fileInput = ref(null)

const triggerInput = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  if (event.target.files.length > 0) {
    emit('files-selected', Array.from(event.target.files))
    // Reset input so same files can be selected again if needed (though accumulation is handled by parent)
    event.target.value = ''
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  if (event.dataTransfer.files.length > 0) {
    emit('files-selected', Array.from(event.dataTransfer.files))
  }
}
</script>

<template>
  <div 
    class="upload-box" 
    @click="triggerInput" 
    @dragover.prevent 
    @drop="handleDrop"
  >
    <input 
      type="file" 
      ref="fileInput" 
      accept=".pdf, .ppt, .pptx, audio/*" 
      multiple 
      hidden
      @change="handleFileChange"
    >
    <div class="icon">📁</div>
    <p>點擊選擇檔案，或拖放至此</p>
    <div class="hint">支援 PDF, PPT, MP3, WAV, M4A</div>
  </div>
</template>

<style scoped>
.upload-box {
    border: 2px dashed #d1d5db;
    border-radius: 14px;
    padding: 32px 20px;
    text-align: center;
    background: #f9fafb;
    margin-bottom: 24px;
    transition: all 0.2s;
    cursor: pointer;
    position: relative;
    user-select: none;
}

.upload-box:hover {
    border-color: #4f46e5;
    background: #f5f3ff;
}

.upload-box p {
    margin: 8px 0 4px;
    font-size: 16px;
    font-weight: 500;
    color: #374151;
}

.icon {
    font-size: 48px; 
    margin-bottom: 16px;
}

.hint {
    margin-top: 8px;
    font-size: 12px;
    color: #9ca3af;
}
</style>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: {
    type: Object,
    required: true
  }
})

const statusClass = computed(() => {
  if (props.result.notion_status && props.result.notion_status.includes('Success')) {
    return 'status-success'
  }
  return 'status-error'
})

const statusText = computed(() => {
  if (props.result.notion_status && props.result.notion_status.includes('Success')) {
    return 'Notion 同步成功'
  }
  return props.result.notion_status || '未知錯誤'
})
</script>

<template>
  <div class="result-box">
    <h2 class="section-title">分析結果：{{ result.filename }}</h2>

    <span :class="['status-tag', statusClass]">{{ statusText }}</span>

    <h3 class="section-title" style="margin-top: 16px;">摘要內容 (Markdown)</h3>
    <pre class="summary-content">{{ result.summary }}</pre>
  </div>
</template>

<style scoped>
.result-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px;
    margin-top: 20px;
}

.section-title {
    margin: 24px 0 8px;
    font-size: 16px;
    font-weight: 600;
    color: #111827;
}

.section-title:first-child {
    margin-top: 0;
}

.status-tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 12px;
}

.status-success {
    background: #dcfce7;
    color: #166534;
}

.status-error {
    background: #fee2e2;
    color: #991b1b;
}

pre.summary-content {
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    max-height: 400px;
    overflow: auto;
    font-size: 14px;
    white-space: pre-wrap;
    margin: 0;
}
</style>

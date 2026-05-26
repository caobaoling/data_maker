<template>
  <div class="hosts-viewer">
    <el-card v-loading="loading">
      <template #header>
        <span><strong>Hosts 文件</strong></span>
      </template>

      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane
          v-for="file in files"
          :key="file.filename"
          :label="file.name"
          :name="file.filename">
          <div class="code-toolbar">
            <el-button
              type="primary"
              size="small"
              :icon="DocumentCopy"
              @click="copyContent(file.content, file.name)">
              一键复制
            </el-button>
          </div>
          <pre class="code-block"><code>{{ file.content }}</code></pre>
        </el-tab-pane>
      </el-tabs>

      <el-empty v-if="!loading && files.length === 0" description="暂无 hosts 文件" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentCopy } from '@element-plus/icons-vue'
import { getHostsFiles } from '@/api/tools'

const loading = ref(false)
const files = ref([])
const activeTab = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const res = await getHostsFiles()
    if (res.code === '0') {
      files.value = res.data
      if (res.data.length > 0) {
        activeTab.value = res.data[0].filename
      }
    } else {
      ElMessage.error(res.msg || '获取失败')
    }
  } catch (e) {
    ElMessage.error('请求异常')
  } finally {
    loading.value = false
  }
})

const copyContent = (content, name) => {
  // navigator.clipboard 仅在 HTTPS/localhost 下可用，兼容 HTTP IP 访问
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(content).then(() => {
      ElMessage.success(`已复制「${name}」内容`)
    }).catch(() => {
      fallbackCopy(content, name)
    })
  } else {
    fallbackCopy(content, name)
  }
}

const fallbackCopy = (content, name) => {
  const textarea = document.createElement('textarea')
  textarea.value = content
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.focus()
  textarea.select()
  try {
    document.execCommand('copy')
    ElMessage.success(`已复制「${name}」内容`)
  } catch {
    ElMessage.error('复制失败，请手动选择复制')
  } finally {
    document.body.removeChild(textarea)
  }
}
</script>

<style scoped>
.hosts-viewer {
  height: 100%;
}

.code-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.code-block {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 16px 20px;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre;
  max-height: 68vh;
  overflow-y: auto;
  margin: 0;
}

/* 注释行高亮 */
.code-block :deep(code) {
  display: block;
}
</style>

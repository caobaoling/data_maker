<template>
  <div class="url-unquote">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>转义URL</strong>URL解码工具</span>
          <el-tag type="info">本地工具</el-tag>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="section-title">URL编码（带%的URL）</div>
          <el-input
            v-model="encodedUrl"
            type="textarea"
            :rows="8"
            placeholder="请输入需要解码的URL，例如：https://example.com?param=value%20test"
            clearable>
          </el-input>
          <div class="button-group">
            <el-button type="primary" @click="decodeUrl">
              <el-icon><Link /></el-icon>
              解码URL
            </el-button>
            <el-button @click="clearAll">
              <el-icon><Delete /></el-icon>
              清空
            </el-button>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="section-title">解码结果</div>
          <el-input
            v-model="decodedUrl"
            type="textarea"
            :rows="8"
            placeholder="解码后的URL将显示在这里"
            readonly>
          </el-input>
          <div class="button-group">
            <el-button type="success" @click="copyResult">
              <el-icon><CopyDocument /></el-icon>
              复制结果
            </el-button>
            <el-button type="warning" @click="openUrl" :disabled="!decodedUrl">
              <el-icon><View /></el-icon>
              打开链接
            </el-button>
          </div>
        </el-col>
      </el-row>

      <el-divider>使用说明</el-divider>
      <el-alert
        title="功能说明"
        type="info"
        :closable="false">
        <template #default>
          <ol>
            <li>将URL编码（带%符号的URL）粘贴到左侧输入框</li>
            <li>点击"解码URL"按钮</li>
            <li>右侧会显示解码后的可读URL</li>
            <li>点击"复制结果"可复制解码后的URL</li>
            <li>点击"打开链接"可在新标签页中打开URL</li>
          </ol>
        </template>
      </el-alert>

      <el-divider>示例</el-divider>
      <el-card shadow="never" class="example-card">
        <template #header>
          <span>示例URL</span>
        </template>
        <div class="example-content">
          <p><strong>编码前：</strong></p>
          <el-input v-model="exampleEncoded" readonly type="textarea" :rows="2" />
          <p style="margin-top: 10px;"><strong>解码后：</strong></p>
          <el-input v-model="exampleDecoded" readonly type="textarea" :rows="2" />
          <el-button type="primary" size="small" @click="useExample" style="margin-top: 10px;">
            使用此示例
          </el-button>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Link, Delete, CopyDocument, View } from '@element-plus/icons-vue'

const encodedUrl = ref('')
const decodedUrl = ref('')

// 示例数据
const exampleEncoded = ref('https://appkidi.51suyang.cn/User/userAutoLogin?link=https%3A%2F%2Fresources.51suyang.cn%2FPictureBook%2FApi%2FPictureBook%2FlistHtml%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNTgwMjQyNDUifQ.AHn7noRvae9G7Z4-E1PnwbH50vzzJ1N94akZBQ2DqhU%26version%3D6.4.0%26systemVer%3D14.2%26device_firm%3DApple%26resource_domain%3Dresources.51suyang.cn')
const exampleDecoded = ref('https://appkidi.51suyang.cn/User/userAutoLogin?link=https://resources.51suyang.cn/PictureBook/Api/PictureBook/listHtml?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNTgwMjQyNDUifQ.AHn7noRvae9G7Z4-E1PnwbH50vzzJ1N94akZBQ2DqhU&version=6.4.0&systemVer=14.2&device_firm=Apple&resource_domain=resources.51suyang.cn')

const decodeUrl = () => {
  try {
    if (!encodedUrl.value) {
      ElMessage.warning('请输入需要解码的URL')
      return
    }

    // 使用JavaScript的decodeURIComponent进行URL解码
    decodedUrl.value = decodeURIComponent(encodedUrl.value)
    ElMessage.success('URL解码完成')
  } catch (error) {
    ElMessage.error('URL解码失败：' + error.message)
  }
}

const copyResult = () => {
  if (!decodedUrl.value) {
    ElMessage.warning('没有可复制的内容')
    return
  }

  navigator.clipboard.writeText(decodedUrl.value).then(() => {
    ElMessage.success('结果已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

const openUrl = () => {
  if (!decodedUrl.value) {
    ElMessage.warning('没有可打开的链接')
    return
  }

  window.open(decodedUrl.value, '_blank')
}

const clearAll = () => {
  encodedUrl.value = ''
  decodedUrl.value = ''
  ElMessage.success('已清空')
}

const useExample = () => {
  encodedUrl.value = exampleEncoded.value
  decodedUrl.value = exampleDecoded.value
  ElMessage.success('已加载示例')
}
</script>

<style scoped>
.url-unquote {
  padding: 0;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-weight: bold;
  margin-bottom: 10px;
  color: #606266;
}

.button-group {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

ol {
  margin: 0;
  padding-left: 20px;
}

li {
  margin-bottom: 5px;
}

.example-card {
  background-color: #f5f7fa;
}

.example-content {
  font-size: 14px;
}

.example-content p {
  margin: 5px 0;
  color: #606266;
}
</style>

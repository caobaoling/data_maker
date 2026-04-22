<template>
  <div class="wordcloud-page">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>词云生成</strong>文本关键词可视化</span>
          <el-tag type="info">基于 jieba + wordcloud</el-tag>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="文本内容" prop="text">
          <el-input
            v-model="form.text"
            type="textarea"
            :rows="8"
            placeholder="请输入要分析的文本内容，系统将自动提取关键词生成词云"
            clearable>
          </el-input>
        </el-form-item>

        <el-form-item label="最大词数" prop="maxWords">
          <el-slider v-model="form.maxWords" :min="50" :max="300" :step="10" show-stops />
        </el-form-item>

        <el-form-item label="图片宽度" prop="width">
          <el-input-number v-model="form.width" :min="400" :max="2400" :step="100" />
        </el-form-item>

        <el-form-item label="图片高度" prop="height">
          <el-input-number v-model="form.height" :min="300" :max="1200" :step="100" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="generating" @click="handleGenerate">
            生成词云
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 词云结果展示 -->
    <el-card v-if="result" class="result-card">
      <template #header>
        <div class="card-header">
          <span>词云结果</span>
          <el-tag :type="result.success ? 'success' : 'danger'">
            {{ result.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <div v-if="result.success" class="wordcloud-result">
        <div class="image-container">
          <img :src="result.imageUrl" alt="词云图" class="wordcloud-image" />
        </div>
        <div class="actions">
          <el-button type="primary" @click="downloadImage">
            <el-icon><Download /></el-icon>
            下载图片
          </el-button>
        </div>
        
        <!-- 关键词列表 -->
        <el-divider>关键词统计</el-divider>
        <div class="keywords-list">
          <el-tag
            v-for="(item, index) in result.keywords"
            :key="index"
            :type="getTagType(index)"
            class="keyword-tag"
            size="large">
            {{ item.word }} ({{ item.count }})
          </el-tag>
        </div>
      </div>

      <el-alert
        v-else
        :title="result.message || '生成失败'"
        type="error"
        :closable="false"
        show-icon />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import { generateWordCloud } from '@/api/tools'

const formRef = ref(null)

const form = reactive({
  text: '',
  maxWords: 150,
  width: 1600,
  height: 800
})

const rules = {
  text: [
    { required: true, message: '请输入文本内容', trigger: 'blur' },
    { min: 50, message: '文本内容至少需要50个字符', trigger: 'blur' }
  ]
}

const generating = ref(false)
const result = ref(null)

const handleGenerate = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    generating.value = true
    result.value = null

    const res = await generateWordCloud({
      text: form.text,
      max_words: form.maxWords,
      width: form.width,
      height: form.height
    })

    if (res.code === '0') {
      result.value = {
        success: true,
        imageUrl: res.data?.image_url,
        keywords: res.data?.keywords || []
      }
      ElMessage.success('词云生成成功')
    } else {
      result.value = {
        success: false,
        message: res.msg || '生成失败'
      }
      ElMessage.error(res.msg || '生成失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    generating.value = false
  }
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  result.value = null
}

const downloadImage = () => {
  if (!result.value?.imageUrl) return
  
  const link = document.createElement('a')
  link.href = result.value.imageUrl
  link.download = `wordcloud_${Date.now()}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  ElMessage.success('图片下载中...')
}

const getTagType = (index) => {
  const types = ['danger', 'warning', 'success', 'info', 'primary']
  return types[index % types.length]
}
</script>

<style scoped>
.wordcloud-page {
  padding: 0;
}

.form-card {
  margin-bottom: 20px;
}

.result-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.wordcloud-result {
  padding: 10px 0;
}

.image-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
}

.wordcloud-image {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.keywords-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.keyword-tag {
  font-size: 14px;
}
</style>

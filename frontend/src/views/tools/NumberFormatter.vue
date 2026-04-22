<template>
  <div class="number-formatter">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>数字格式化</strong>Excel数据格式化工具</span>
          <el-tag type="info">本地工具</el-tag>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="section-title">输入数据（从Excel复制的数据）</div>
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="12"
            placeholder="请粘贴从Excel复制的数据，每行一个或多个数字"
            clearable>
          </el-input>
          <div class="button-group">
            <el-button type="primary" @click="formatNumbers">
              <el-icon><Grid /></el-icon>
              格式化
            </el-button>
            <el-button @click="clearAll">
              <el-icon><Delete /></el-icon>
              清空
            </el-button>
          </div>
        </el-col>

        <el-col :span="12">
          <div class="section-title">格式化结果</div>
          <el-input
            v-model="outputText"
            type="textarea"
            :rows="12"
            placeholder="格式化后的结果将显示在这里"
            readonly>
          </el-input>
          <div class="button-group">
            <el-button type="success" @click="copyResult">
              <el-icon><CopyDocument /></el-icon>
              复制结果
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
            <li>从Excel中复制数字数据</li>
            <li>粘贴到左侧输入框</li>
            <li>点击"格式化"按钮</li>
            <li>工具会自动将数字用逗号连接，并去掉小数点后的.0</li>
            <li>点击"复制结果"可复制格式化后的内容</li>
          </ol>
        </template>
      </el-alert>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Grid, Delete, CopyDocument } from '@element-plus/icons-vue'

const inputText = ref('')
const outputText = ref('')

const formatNumbers = () => {
  try {
    const inputData = inputText.value.trim()
    if (!inputData) {
      ElMessage.warning('请输入数据')
      return
    }

    const lines = inputData.split('\n')
    const formattedNumbers = []

    for (const line of lines) {
      // 分割每行的数字
      const numbers = line.split(/\s+/)
      for (const num of numbers) {
        if (!num.trim()) continue
        
        try {
          // 尝试转换为浮点数并去掉小数点后的.0
          const floatNum = parseFloat(num)
          if (!isNaN(floatNum)) {
            if (Number.isInteger(floatNum)) {
              formattedNumbers.push(String(floatNum))
            } else {
              formattedNumbers.push(String(floatNum))
            }
          } else {
            // 如果不是数字，保持原样
            formattedNumbers.push(num)
          }
        } catch (e) {
          // 如果不是数字，保持原样
          formattedNumbers.push(num)
        }
      }
    }

    // 用逗号连接所有数字并显示结果
    outputText.value = formattedNumbers.join(',')
    ElMessage.success('格式化完成')
  } catch (error) {
    ElMessage.error('格式化失败：' + error.message)
  }
}

const copyResult = () => {
  if (!outputText.value) {
    ElMessage.warning('没有可复制的内容')
    return
  }

  navigator.clipboard.writeText(outputText.value).then(() => {
    ElMessage.success('结果已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

const clearAll = () => {
  inputText.value = ''
  outputText.value = ''
  ElMessage.success('已清空')
}
</script>

<style scoped>
.number-formatter {
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
</style>

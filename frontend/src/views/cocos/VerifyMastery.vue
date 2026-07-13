<template>
  <div class="verify-mastery">
    <el-card>
      <template #header>
        <span>线上环境课后出题校验</span>
      </template>

      <el-form :model="form" label-width="90px" @submit.prevent="handleSubmit">
        <el-form-item label="约课ID" required>
          <el-input
            v-model="form.appoint_id"
            placeholder="请输入约课ID，如 539673674"
            clearable
            style="width: 300px"
          />
        </el-form-item>

        <el-form-item label="课程类型">
          <el-select
            v-model="form.lesson_type"
            placeholder="不填则校验全部知识点"
            clearable
            style="width: 240px"
          >
            <el-option label="词汇句型课 (vocabulary_class)"   value="vocabulary_class" />
            <el-option label="对话课 (conversation_class)"     value="conversation_class" />
            <el-option label="阅读课 (reading_class)"          value="reading_class" />
            <el-option label="字母课 (alphabet_class)"         value="alphabet_class" />
            <el-option label="自拼课 (phonics_class)"          value="phonics_class" />
            <el-option label="嘉年华 (carnival_class)"         value="carnival_class" />
          </el-select>
        </el-form-item>

        <el-form-item label="课程级别">
          <el-select
            v-model="form.lesson_level"
            placeholder="不填则校验全部知识点"
            clearable
            style="width: 160px"
          >
            <el-option label="Level 0" value="Level 0" />
            <el-option label="Level 1" value="Level 1" />
            <el-option label="Level 2" value="Level 2" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="running" @click="handleSubmit">
            {{ running ? '执行中...' : '开始校验' }}
          </el-button>
          <el-button :disabled="running" @click="handleClear">清空结果</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 输出区域 -->
    <el-card v-if="output || running" style="margin-top: 16px">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>执行输出</span>
          <el-tag v-if="running" type="warning" effect="plain">执行中</el-tag>
          <el-tag v-else-if="output" type="success" effect="plain">完成</el-tag>
        </div>
      </template>
      <pre class="output-pre" ref="outputRef">{{ output }}</pre>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { verifyMastery } from '@/api/cocos'

const form = ref({
  appoint_id:   '',
  lesson_type:  '',
  lesson_level: '',
})

const running   = ref(false)
const output    = ref('')
const outputRef = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (outputRef.value) {
      outputRef.value.scrollTop = outputRef.value.scrollHeight
    }
  })
}

const handleSubmit = async () => {
  if (!form.value.appoint_id.trim()) {
    ElMessage.warning('请填写约课ID')
    return
  }
  if ((form.value.lesson_type && !form.value.lesson_level) ||
      (!form.value.lesson_type && form.value.lesson_level)) {
    ElMessage.warning('课程类型和课程级别需同时填写或同时留空')
    return
  }

  running.value = true
  output.value  = ''

  try {
    await verifyMastery(
      {
        appoint_id:   form.value.appoint_id.trim(),
        lesson_type:  form.value.lesson_type,
        lesson_level: form.value.lesson_level,
      },
      (chunk) => {
        output.value += chunk
        scrollToBottom()
      }
    )
  } catch (e) {
    ElMessage.error(e.message || '执行失败')
    output.value += `\n[错误] ${e.message}\n`
  } finally {
    running.value = false
    scrollToBottom()
  }
}

const handleClear = () => {
  output.value = ''
}
</script>

<style scoped>
.verify-mastery {
  max-width: 960px;
}

.output-pre {
  margin: 0;
  padding: 12px;
  background: #1e1e1e;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.6;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 600px;
  overflow-y: auto;
}
</style>

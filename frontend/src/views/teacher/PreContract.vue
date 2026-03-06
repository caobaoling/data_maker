<template>
  <div class="pre-contract">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>给老师签合同(SA)</span>
          <el-tag type="info">为老师添加合同签约记录</el-tag>
        </div>
      </template>

      <!-- 添加表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="老师ID" prop="teacher_id">
          <el-input
            v-model="form.teacher_id"
            placeholder="请输入老师ID"
            clearable
            style="width: 400px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            添加合同
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作结果展示 -->
    <el-card v-if="result" class="result-card">
      <template #header>
        <div class="card-header">
          <span>操作日志</span>
          <el-tag :type="result.success ? 'success' : 'danger'">
            {{ result.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <el-timeline>
        <el-timeline-item
          v-for="step in result.steps"
          :key="step.step"
          :type="step.success ? 'success' : 'danger'"
          :icon="step.success ? 'CircleCheck' : 'CircleClose'"
        >
          <div class="log-item">
            <div class="log-title">
              <span class="step-name">步骤{{ step.step }}: {{ step.name }}</span>
              <el-tag :type="step.success ? 'success' : 'danger'" size="small">
                {{ step.success ? '成功' : '失败' }}
              </el-tag>
            </div>
            <div class="log-content">{{ step.log }}</div>
            <div v-if="step.sa_end_time" class="log-detail">
              SA结束时间: {{ step.sa_end_time }}
            </div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { addPreContract } from '@/api/teacher'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  teacher_id: ''
})

// 表单验证规则
const rules = {
  teacher_id: [
    { required: true, message: '请输入老师ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '老师ID必须是数字', trigger: 'blur' }
  ]
}

// 提交状态
const submitting = ref(false)

// 操作结果
const result = ref(null)

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true
    result.value = null

    const res = await addPreContract({
      teacher_id: form.teacher_id
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '添加成功')
      result.value = res.data
    } else {
      ElMessage.error(res.msg || '添加失败')
      result.value = res.data || { success: false, message: res.msg }
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    submitting.value = false
  }
}

// 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  result.value = null
}
</script>

<style scoped>
.pre-contract {
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

.log-item {
  padding: 10px 0;
}

.log-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.step-name {
  font-weight: 600;
  font-size: 14px;
}

.log-content {
  color: #606266;
  font-size: 13px;
  line-height: 1.6;
  margin-bottom: 5px;
}

.log-detail {
  color: #909399;
  font-size: 12px;
}
</style>

<template>
  <div class="teacher-email">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>查看老师邮箱</span>
          <el-tag type="info">查询老师邮箱信息</el-tag>
        </div>
      </template>

      <!-- 查询表单 -->
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
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            查询邮箱
          </el-button>
          <el-button type="warning" :loading="resetLoading" @click="handleResetPassword">
            重置密码
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 查询结果展示 -->
    <el-card v-if="result" class="result-card">
      <template #header>
        <div class="card-header">
          <span>查询结果</span>
          <el-tag :type="result.success ? 'success' : 'danger'">
            {{ result.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <div v-if="result.success && result.email" class="email-result">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="老师ID">
            <el-tag size="small">{{ result.teacher_id }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="邮箱地址">
            <div class="email-address">
              <span class="email-text">{{ result.email }}</span>
              <el-button
                type="primary"
                size="small"
                :icon="CopyDocument"
                @click="copyEmail(result.email)">
                复制
              </el-button>
            </div>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <el-alert
        v-else-if="!result.success"
        :title="result.message || '查询失败'"
        type="error"
        :closable="false"
        show-icon />

      <el-alert
        v-else
        title="未找到该老师的邮箱信息"
        type="warning"
        :closable="false"
        show-icon />
    </el-card>

    <!-- 重置密码结果展示 -->
    <el-card v-if="resetResult" class="result-card">
      <template #header>
        <div class="card-header">
          <span>重置密码结果</span>
          <el-tag :type="resetResult.success ? 'success' : 'danger'">
            {{ resetResult.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <el-alert
        :title="resetResult.message"
        :type="resetResult.success ? 'success' : 'error'"
        :closable="false"
        show-icon />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, CopyDocument } from '@element-plus/icons-vue'
import { getTeacherEmail, resetTeacherPassword } from '@/api/teacher'

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

// 加载状态
const loading = ref(false)
const resetLoading = ref(false)

// 查询结果
const result = ref(null)
const resetResult = ref(null)

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    loading.value = true
    result.value = null

    const res = await getTeacherEmail({
      teacher_id: form.teacher_id
    })

    if (res.code === '0') {
      result.value = {
        success: true,
        teacher_id: form.teacher_id,
        email: res.data?.email || res.data?.data?.email
      }
    } else {
      result.value = {
        success: false,
        message: res.msg || '查询失败'
      }
      ElMessage.error(res.msg || '查询失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    loading.value = false
  }
}

// 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  result.value = null
  resetResult.value = null
}

// 重置密码
const handleResetPassword = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    resetLoading.value = true
    resetResult.value = null

    const res = await resetTeacherPassword({
      teacher_id: form.teacher_id
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '重置密码成功')
      resetResult.value = {
        success: true,
        message: res.msg || '重置密码成功'
      }
    } else {
      resetResult.value = {
        success: false,
        message: res.msg || '重置密码失败'
      }
      ElMessage.error(res.msg || '重置密码失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    resetLoading.value = false
  }
}

// 复制邮箱到剪贴板
const copyEmail = (email) => {
  navigator.clipboard.writeText(email).then(() => {
    ElMessage.success('邮箱已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败，请手动复制')
  })
}
</script>

<style scoped>
.teacher-email {
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

.email-result {
  padding: 10px 0;
}

.email-address {
  display: flex;
  align-items: center;
  gap: 15px;
}

.email-text {
  font-size: 16px;
  font-weight: 500;
  color: #409eff;
  font-family: monospace;
}
</style>

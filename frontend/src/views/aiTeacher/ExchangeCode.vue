<template>
  <div class="exchange-code">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>使用兑换码</span>
          <el-tag type="warning">为用户兑换AI外教权益</el-tag>
        </div>
      </template>

      <!-- 使用表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <HistoryInput
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            storage-key="exchange-code_user_id"
            style="width: 500px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </HistoryInput>
        </el-form-item>

        <el-form-item label="兑换码" prop="exchange_code">
          <HistoryInput
            v-model="form.exchange_code"
            placeholder="请输入兑换码，如: 37e6d355095ce3973e11f65d3949b8fa"
            clearable
            storage-key="exchange-code_exchange_code"
            style="width: 500px">
            <template #prepend>
              <el-icon><Ticket /></el-icon>
            </template>
          </HistoryInput>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            立即兑换
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 说明信息 -->
      <el-alert type="info" :closable="false" style="margin-top: 20px">
        <template #title>
          <strong>兑换说明</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li>兑换码由运营人员或系统生成</li>
          <li>每个兑换码只能使用一次</li>
          <li>兑换成功后会自动添加对应权益到用户账户</li>
          <li>兑换失败可能是因为兑换码已被使用或不存在</li>
        </ul>
      </el-alert>

      <!-- 待完善提示 -->
      <el-alert type="warning" :closable="false" style="margin-top: 10px">
        <template #title>
          <strong>⚠️ 功能待完善</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li>兑换码生成功能待开发</li>
          <li>兑换记录查询功能待开发</li>
          <li>兑换码状态管理待开发</li>
        </ul>
      </el-alert>
    </el-card>

    <!-- 兑换历史记录 -->
    <el-card v-if="historyList.length > 0" class="history-card">
      <template #header>
        <div class="card-header">
          <span>兑换历史</span>
          <el-button text @click="handleClearHistory">清空记录</el-button>
        </div>
      </template>

      <el-timeline>
        <el-timeline-item
          v-for="(item, index) in historyList"
          :key="index"
          :timestamp="item.timestamp"
          :type="item.success ? 'success' : 'danger'"
          placement="top">
          <el-card>
            <div class="history-item">
              <div class="history-info">
                <div>
                  <el-tag :type="item.success ? 'success' : 'danger'" size="small">
                    {{ item.success ? '兑换成功' : '兑换失败' }}
                  </el-tag>
                  <span style="margin-left: 10px">用户ID: {{ item.user_id }}</span>
                </div>
                <div style="margin-top: 5px">
                  兑换码: <el-tag type="info" size="small">{{ item.exchange_code }}</el-tag>
                </div>
                <div v-if="item.message" style="margin-top: 5px; color: #909399; font-size: 12px">
                  {{ item.message }}
                </div>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Ticket } from '@element-plus/icons-vue'
import { useExchangeCode } from '@/api/aiTeacher'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  user_id: '',
  exchange_code: ''
})

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  exchange_code: [
    { required: true, message: '请输入兑换码', trigger: 'blur' },
    { min: 10, message: '兑换码长度至少10位', trigger: 'blur' }
  ]
}

// 提交状态
const submitting = ref(false)

// 兑换历史记录
const historyList = ref([])

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true

    const res = await useExchangeCode({
      user_id: form.user_id,
      exchange_code: form.exchange_code
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '兑换成功')

      // 添加到历史记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        user_id: form.user_id,
        exchange_code: form.exchange_code,
        success: true,
        message: res.msg
      })

      // 清空表单
      form.exchange_code = ''
    } else {
      ElMessage.error(res.msg || '兑换失败')

      // 添加失败记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        user_id: form.user_id,
        exchange_code: form.exchange_code,
        success: false,
        message: res.msg
      })
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
}

// 清空历史记录
const handleClearHistory = () => {
  historyList.value = []
  ElMessage.success('已清空历史记录')
}
</script>

<style scoped>
.exchange-code {
  padding: 0;
}

.form-card {
  margin-bottom: 20px;
}

.history-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-info {
  flex: 1;
}
</style>

<template>
  <div class="end-class">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>精灵结课</span>
          <el-tag type="primary">触发精灵结课结算</el-tag>
        </div>
      </template>

      <!-- 结课表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            style="width: 500px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="业务ID" prop="biz_id">
          <el-input
            v-model="form.biz_id"
            placeholder="请输入业务ID（约课ID）"
            clearable
            style="width: 500px">
            <template #prepend>
              <el-icon><Document /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            执行结课
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 说明信息 -->
      <el-alert type="info" :closable="false" style="margin-top: 20px">
        <template #title>
          <strong>功能说明</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li>触发精灵系统的结课结算流程</li>
          <li>业务ID通常为预约ID（约课ID）</li>
          <li>结课后会更新用户的精灵数据和排行榜数据</li>
          <li>结算类型: type=2</li>
        </ul>
      </el-alert>
    </el-card>

    <!-- 操作历史 -->
    <el-card v-if="historyList.length > 0" class="history-card">
      <template #header>
        <div class="card-header">
          <span>操作历史</span>
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
                    {{ item.success ? '结课成功' : '结课失败' }}
                  </el-tag>
                  <span style="margin-left: 10px">用户ID: {{ item.user_id }}</span>
                  <span style="margin-left: 10px">业务ID: {{ item.biz_id }}</span>
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
import { User, Document } from '@element-plus/icons-vue'
import { createEndClass } from '@/api/elf'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  user_id: '',
  biz_id: ''
})

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  biz_id: [
    { required: true, message: '请输入业务ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '业务ID必须是数字', trigger: 'blur' }
  ]
}

// 提交状态
const submitting = ref(false)

// 操作历史
const historyList = ref([])

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true

    const res = await createEndClass({
      user_id: form.user_id,
      biz_id: form.biz_id
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '结课成功')

      // 添加到历史记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        user_id: form.user_id,
        biz_id: form.biz_id,
        success: true,
        message: res.msg
      })

      // 清空业务ID，保留用户ID
      form.biz_id = ''
    } else {
      ElMessage.error(res.msg || '结课失败')

      // 添加失败记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        user_id: form.user_id,
        biz_id: form.biz_id,
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
.end-class {
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

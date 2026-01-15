<template>
  <div class="add-star">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>添加星星</span>
          <el-tag type="warning">为课程预约添加星星评分</el-tag>
        </div>
      </template>

      <!-- 添加表单 -->
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

        <el-form-item label="预约ID" prop="appoint_id">
          <el-input
            v-model="form.appoint_id"
            placeholder="请输入预约ID"
            clearable
            style="width: 500px">
            <template #prepend>
              <el-icon><Document /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="星星数量" prop="star_num">
          <el-input-number
            v-model="form.star_num"
            :min="1"
            :max="5"
            style="width: 500px" />
          <span style="margin-left: 10px; color: #909399">默认2颗星</span>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            添加星星
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
          <li>为指定课程预约添加星星评分</li>
          <li>星星数量范围: 1-5颗星</li>
          <li>会触发精灵系统的相关任务和奖励</li>
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
                    {{ item.success ? '添加成功' : '添加失败' }}
                  </el-tag>
                  <span style="margin-left: 10px">用户ID: {{ item.user_id }}</span>
                  <span style="margin-left: 10px">预约ID: {{ item.appoint_id }}</span>
                  <span style="margin-left: 10px">星星数: {{ item.star_num }}</span>
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
import { addStar } from '@/api/elf'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  user_id: '',
  appoint_id: '',
  star_num: 2
})

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  appoint_id: [
    { required: true, message: '请输入预约ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '预约ID必须是数字', trigger: 'blur' }
  ],
  star_num: [
    { required: true, message: '请输入星星数量', trigger: 'blur' }
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

    const res = await addStar({
      user_id: form.user_id,
      appoint_id: form.appoint_id,
      star_num: form.star_num
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '添加成功')

      // 添加到历史记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        user_id: form.user_id,
        appoint_id: form.appoint_id,
        star_num: form.star_num,
        success: true,
        message: res.msg
      })

      // 清空预约ID，保留用户ID
      form.appoint_id = ''
      form.star_num = 2
    } else {
      ElMessage.error(res.msg || '添加失败')

      // 添加失败记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        user_id: form.user_id,
        appoint_id: form.appoint_id,
        star_num: form.star_num,
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
.add-star {
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

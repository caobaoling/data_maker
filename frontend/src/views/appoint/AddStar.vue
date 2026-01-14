<template>
  <div class="add-star-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>预约打星</span>
          <el-tag type="info" size="small">为课程预约添加星级评价</el-tag>
        </div>
      </template>

      <!-- 打星表单 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        style="max-width: 600px">

        <el-form-item label="学生ID" prop="stu_id">
          <el-input
            v-model.number="form.stu_id"
            type="number"
            placeholder="请输入学生ID"
            clearable>
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="预约ID" prop="appoint_id">
          <el-input
            v-model.number="form.appoint_id"
            type="number"
            placeholder="请输入预约ID"
            clearable>
            <template #prepend>
              <el-icon><Ticket /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="星级评价" prop="star_num">
          <div style="display: flex; align-items: center; gap: 15px;">
            <el-rate
              v-model="form.star_num"
              :max="5"
              size="large"
              show-text
              :texts="['极差', '失望', '一般', '满意', '惊喜']" />
            <el-tag :type="getStarTagType(form.star_num)" size="large">
              {{ form.star_num }} 星
            </el-tag>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleSubmit"
            size="large"
            icon="Star">
            提交评价
          </el-button>
          <el-button @click="handleReset" size="large" icon="RefreshRight">
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 结果提示卡片 -->
      <el-card v-if="result" class="result-card" :type="result.success ? 'success' : 'danger'">
        <template #header>
          <div style="display: flex; align-items: center; gap: 10px;">
            <el-icon :size="20" :color="result.success ? '#67c23a' : '#f56c6c'">
              <SuccessFilled v-if="result.success" />
              <CircleCloseFilled v-else />
            </el-icon>
            <span>{{ result.success ? '打星成功' : '打星失败' }}</span>
          </div>
        </template>
        <div class="result-content">
          <p><strong>学生ID:</strong> {{ result.stu_id }}</p>
          <p><strong>预约ID:</strong> {{ result.appoint_id }}</p>
          <p><strong>星级:</strong>
            <el-rate v-model="result.star_num" disabled />
          </p>
          <p v-if="!result.success" style="color: #f56c6c;">
            <strong>错误信息:</strong> {{ result.message }}
          </p>
        </div>
      </el-card>

      <!-- 使用说明 -->
      <el-alert
        title="使用说明"
        type="info"
        :closable="false"
        style="margin-top: 30px;">
        <ul style="margin: 0; padding-left: 20px;">
          <li>输入有效的学生ID和预约ID</li>
          <li>选择1-5星进行评价（5星最高）</li>
          <li>提交后会调用打星API为预约添加评价</li>
          <li>可在预约列表中查看打星结果</li>
        </ul>
      </el-alert>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Ticket, Star, RefreshRight, SuccessFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import { addAppointStar } from '@/api/appoint'

const formRef = ref(null)
const loading = ref(false)
const result = ref(null)

const form = reactive({
  stu_id: null,
  appoint_id: null,
  star_num: 5
})

const rules = {
  stu_id: [
    { required: true, message: '请输入学生ID', trigger: 'blur' },
    { type: 'number', message: '学生ID必须是数字', trigger: 'blur' }
  ],
  appoint_id: [
    { required: true, message: '请输入预约ID', trigger: 'blur' },
    { type: 'number', message: '预约ID必须是数字', trigger: 'blur' }
  ],
  star_num: [
    { required: true, message: '请选择星级', trigger: 'change' }
  ]
}

// 根据星级返回标签类型
const getStarTagType = (stars) => {
  if (stars <= 2) return 'danger'
  if (stars === 3) return 'warning'
  if (stars === 4) return 'primary'
  return 'success'
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch (error) {
    ElMessage.warning('请填写完整的表单信息')
    return
  }

  loading.value = true
  result.value = null

  try {
    const response = await addAppointStar({
      stu_id: form.stu_id,
      appoint_id: form.appoint_id,
      star_num: form.star_num
    })

    if (response.code === '10000') {
      ElMessage.success('打星成功！')
      result.value = {
        success: true,
        stu_id: form.stu_id,
        appoint_id: form.appoint_id,
        star_num: form.star_num
      }
    } else {
      ElMessage.error(`打星失败: ${response.message}`)
      result.value = {
        success: false,
        stu_id: form.stu_id,
        appoint_id: form.appoint_id,
        star_num: form.star_num,
        message: response.message
      }
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
    result.value = {
      success: false,
      stu_id: form.stu_id,
      appoint_id: form.appoint_id,
      star_num: form.star_num,
      message: error.message
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  form.stu_id = null
  form.appoint_id = null
  form.star_num = 5
  result.value = null
  formRef.value?.clearValidate()
}
</script>

<style scoped>
.add-star-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-card {
  margin-top: 30px;
}

.result-content p {
  margin: 10px 0;
  font-size: 14px;
  line-height: 1.8;
}

:deep(.el-rate__text) {
  font-size: 14px;
  color: #606266;
}

:deep(.el-input-group__prepend) {
  padding: 0 15px;
}
</style>

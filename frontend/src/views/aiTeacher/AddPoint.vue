<template>
  <div class="add-point">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>添加AI财富</span>
          <el-tag type="info">为用户添加AI外教点数</el-tag>
        </div>
      </template>

      <!-- 添加表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <HistoryInput
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            storage-key="add-point_user_id"
            style="width: 400px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </HistoryInput>
        </el-form-item>

        <el-form-item label="点数数量" prop="count">
          <el-input-number
            v-model="form.count"
            :min="1"
            :max="10000"
            :step="100"
            style="width: 400px" />
          <span style="margin-left: 10px; color: #909399">默认100点</span>
        </el-form-item>

        <el-form-item label="有效天数" prop="days">
          <el-input-number
            v-model="form.days"
            :min="1"
            :max="3650"
            :step="30"
            style="width: 400px" />
          <span style="margin-left: 10px; color: #909399">默认300天</span>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            添加点数
          </el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="info" @click="handleQuery">查询点数</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 查询结果展示 -->
    <el-card v-if="queryResult" class="result-card">
      <template #header>
        <div class="card-header">
          <span>查询结果</span>
          <el-tag type="success">用户 {{ queryResult.user_id }}</el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="总点数">
          <el-tag type="info" size="large">{{ queryResult.total_count }} 点</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="有效点数">
          <el-tag type="warning" size="large">{{ getValidCount() }} 点</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="记录数">
          {{ queryResult.assets.length }} 条
        </el-descriptions-item>
        <el-descriptions-item label="有效记录">
          {{ getValidRecordsCount() }} 条
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">点数明细</el-divider>

      <el-table :data="queryResult.assets" stripe border max-height="400">
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="count" label="点数" width="120">
          <template #default="{ row }">
            <el-tag type="success">{{ row.count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row)">{{ getStatusText(row) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="valid_start" label="生效日期" width="150" />
        <el-table-column prop="valid_end" label="到期日期" width="150" />
        <el-table-column prop="days" label="有效天数" width="120" />
        <el-table-column prop="id" label="记录ID" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { addPoint, queryPoint } from '@/api/aiTeacher'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  user_id: '',
  count: 100,
  days: 300
})

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  count: [
    { required: true, message: '请输入点数数量', trigger: 'blur' }
  ],
  days: [
    { required: true, message: '请输入有效天数', trigger: 'blur' }
  ]
}

// 提交状态
const submitting = ref(false)

// 查询结果
const queryResult = ref(null)

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true

    const res = await addPoint({
      user_id: form.user_id,
      count: form.count,
      days: form.days
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '添加成功')

      // 添加成功后自动查询
      setTimeout(() => {
        handleQuery()
      }, 500)
    } else {
      ElMessage.error(res.msg || '添加失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    submitting.value = false
  }
}

// 查询点数
const handleQuery = async () => {
  if (!form.user_id) {
    ElMessage.warning('请先输入用户ID')
    return
  }

  try {
    const res = await queryPoint({
      user_id: form.user_id
    })

    if (res.code === '0') {
      queryResult.value = res.data
      ElMessage.success('查询成功')
    } else {
      ElMessage.error(res.msg || '查询失败')
    }
  } catch (error) {
    ElMessage.error('查询失败')
  }
}

// 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  queryResult.value = null
}

// 获取状态文本
const getStatusText = (row) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const startDate = new Date(row.valid_start)
  startDate.setHours(0, 0, 0, 0)

  const endDate = new Date(row.valid_end)
  endDate.setHours(23, 59, 59, 999)

  if (today < startDate) {
    return '未生效'
  } else if (today > endDate) {
    return '已过期'
  } else {
    return '有效'
  }
}

// 获取状态标签类型
const getStatusType = (row) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const startDate = new Date(row.valid_start)
  startDate.setHours(0, 0, 0, 0)

  const endDate = new Date(row.valid_end)
  endDate.setHours(23, 59, 59, 999)

  if (today < startDate) {
    return 'info'     // 未生效 - 灰色
  } else if (today > endDate) {
    return 'danger'   // 已过期 - 红色
  } else {
    return 'success'  // 有效 - 绿色
  }
}

// 计算有效点数总和
const getValidCount = () => {
  if (!queryResult.value || !queryResult.value.assets) return 0

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return queryResult.value.assets.reduce((total, row) => {
    const startDate = new Date(row.valid_start)
    startDate.setHours(0, 0, 0, 0)

    const endDate = new Date(row.valid_end)
    endDate.setHours(23, 59, 59, 999)

    // 只计算有效期内的点数
    if (today >= startDate && today <= endDate) {
      return total + parseFloat(row.count)
    }
    return total
  }, 0)
}

// 计算有效记录数量
const getValidRecordsCount = () => {
  if (!queryResult.value || !queryResult.value.assets) return 0

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return queryResult.value.assets.filter(row => {
    const startDate = new Date(row.valid_start)
    startDate.setHours(0, 0, 0, 0)

    const endDate = new Date(row.valid_end)
    endDate.setHours(23, 59, 59, 999)

    // 只计算有效期内的记录
    return today >= startDate && today <= endDate
  }).length
}
</script>

<style scoped>
.add-point {
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
</style>

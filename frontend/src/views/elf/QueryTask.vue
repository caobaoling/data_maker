<template>
  <div class="query-task">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>查询精灵任务</span>
          <el-tag type="info">查询用户的周任务和月任务</el-tag>
        </div>
      </template>

      <!-- 查询表单 -->
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

        <el-form-item>
          <el-button type="primary" :loading="querying" @click="handleQuery">
            查询任务
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
          <li>查询用户的精灵周任务和月任务</li>
          <li>任务分类: elf_week_task（周任务）、elf_month_task（月任务）</li>
          <li>业务类别: game_system</li>
        </ul>
      </el-alert>
    </el-card>

    <!-- 查询结果 -->
    <el-card v-if="taskData" class="result-card">
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <el-tag type="success">用户 {{ taskData.user_id }}</el-tag>
        </div>
      </template>

      <div v-if="!taskData.tasks || taskData.tasks.length === 0">
        <el-empty description="暂无任务数据" />
      </div>

      <div v-else>
        <el-table :data="taskData.tasks" stripe border max-height="600">
          <el-table-column type="index" label="序号" width="80" />
          <el-table-column prop="id" label="任务ID" width="120" />
          <el-table-column label="任务类型" width="150">
            <template #default="{ row }">
              <el-tag :type="getTaskTypeTag(row.task_biz_category)" size="small">
                {{ getTaskTypeName(row.task_biz_category) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="task_name" label="任务名称" show-overflow-tooltip />
          <el-table-column label="进度" width="200">
            <template #default="{ row }">
              <el-progress
                :percentage="getProgress(row.task_progress, row.task_target)"
                :color="getProgressColor(row.task_progress, row.task_target)"
              />
              <div style="text-align: center; font-size: 12px; margin-top: 5px">
                {{ row.task_progress || 0 }} / {{ row.task_target || 0 }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.task_status)" size="small">
                {{ getStatusText(row.task_status) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>

        <el-divider content-position="left">统计信息</el-divider>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-statistic title="总任务数" :value="taskData.tasks.length" />
          </el-col>
          <el-col :span="8">
            <el-statistic
              title="周任务数"
              :value="getTaskCount('elf_week_task')"
              value-style="color: #409eff"
            />
          </el-col>
          <el-col :span="8">
            <el-statistic
              title="月任务数"
              :value="getTaskCount('elf_month_task')"
              value-style="color: #67c23a"
            />
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { queryTask } from '@/api/elf'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  user_id: ''
})

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ]
}

// 查询状态
const querying = ref(false)

// 任务数据
const taskData = ref(null)

// 查询任务
const handleQuery = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    querying.value = true

    const res = await queryTask({
      user_id: form.user_id
    })

    if (res.code === '0') {
      taskData.value = res.data
      ElMessage.success('查询成功')
    } else {
      ElMessage.error(res.msg || '查询失败')
      taskData.value = null
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    querying.value = false
  }
}

// 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  taskData.value = null
}

// 获取任务类型标签
const getTaskTypeTag = (type) => {
  return type === 'elf_week_task' ? 'primary' : 'success'
}

// 获取任务类型名称
const getTaskTypeName = (type) => {
  return type === 'elf_week_task' ? '周任务' : '月任务'
}

// 计算进度百分比
const getProgress = (progress, target) => {
  if (!target || target === 0) return 0
  const percent = (progress / target) * 100
  return Math.min(Math.round(percent), 100)
}

// 获取进度条颜色
const getProgressColor = (progress, target) => {
  const percent = (progress / target) * 100
  if (percent >= 100) return '#67c23a'
  if (percent >= 50) return '#e6a23c'
  return '#909399'
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    0: 'info',      // 未开始
    1: 'primary',   // 进行中
    2: 'success',   // 已完成
    3: 'warning'    // 已领取
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    0: '未开始',
    1: '进行中',
    2: '已完成',
    3: '已领取'
  }
  return statusMap[status] || '未知'
}

// 统计任务数量
const getTaskCount = (type) => {
  if (!taskData.value || !taskData.value.tasks) return 0
  return taskData.value.tasks.filter(task => task.task_biz_category === type).length
}
</script>

<style scoped>
.query-task {
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

<template>
  <div class="del-task">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>删除精灵任务</span>
          <el-tag type="danger">⚠️ 危险操作</el-tag>
        </div>
      </template>

      <!-- 危险操作警告 -->
      <el-alert type="error" :closable="false" style="margin-bottom: 20px">
        <template #title>
          <strong>🚨 危险操作警告</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li><strong>此操作将删除用户的所有精灵任务数据</strong></li>
          <li>包含6个数据表的任务数据（含分表）</li>
          <li><strong style="color: #f56c6c">删除后无法恢复</strong></li>
          <li>请务必确认用户ID正确后再执行</li>
        </ul>
      </el-alert>

      <!-- 删除表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input
            v-model="form.user_id"
            placeholder="请输入要删除任务的用户ID"
            clearable
            style="width: 500px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="danger" :loading="submitting" @click="handleSubmit">
            确认删除
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 将要删除的表列表 -->
      <el-collapse style="margin-top: 20px">
        <el-collapse-item title="查看将要清空的数据表（6个表）" name="1">
          <el-table :data="tableList" stripe border max-height="300">
            <el-table-column type="index" label="序号" width="80" />
            <el-table-column prop="table" label="表名" show-overflow-tooltip />
            <el-table-column prop="description" label="说明" show-overflow-tooltip />
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 删除结果 -->
    <el-card v-if="resultData" class="result-card">
      <template #header>
        <div class="card-header">
          <span>删除结果</span>
          <el-tag :type="resultData.deleted_count > 0 ? 'success' : 'warning'">
            {{ resultData.deleted_count > 0 ? '删除成功' : '无数据' }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border style="margin-bottom: 20px">
        <el-descriptions-item label="用户ID">
          {{ resultData.user_id }}
        </el-descriptions-item>
        <el-descriptions-item label="删除任务数">
          <el-tag type="danger">{{ resultData.deleted_count }} 个</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="成功数" :span="1">
          <el-tag type="success">{{ resultData.deleted_count }} 个</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="失败数" :span="1">
          <el-tag type="warning">{{ resultData.failed_count }} 个</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">删除的任务ID</el-divider>

      <div v-if="resultData.deleted_tasks && resultData.deleted_tasks.length > 0">
        <el-tag
          v-for="(taskId, index) in resultData.deleted_tasks"
          :key="index"
          type="info"
          style="margin: 5px">
          {{ taskId }}
        </el-tag>
      </div>
      <el-empty v-else description="无任务删除" />

      <div v-if="resultData.failed_tasks && resultData.failed_tasks.length > 0" style="margin-top: 20px">
        <el-divider content-position="left">失败任务详情</el-divider>
        <el-table :data="resultData.failed_tasks" stripe border max-height="200">
          <el-table-column type="index" label="序号" width="80" />
          <el-table-column prop="task_id" label="任务ID" width="150" />
          <el-table-column prop="error" label="错误信息" show-overflow-tooltip />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { deleteTask } from '@/api/elf'

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

// 提交状态
const submitting = ref(false)

// 删除结果
const resultData = ref(null)

// 数据表列表
const tableList = [
  { table: 'user_task', description: '用户任务主表' },
  { table: 'user_task_award', description: '用户任务奖励表' },
  { table: 'user_task_XX', description: '用户任务分表（按用户ID后两位）' },
  { table: 'user_task_process_record', description: '任务进度记录表' },
  { table: 'user_award', description: '用户奖励主表' },
  { table: 'user_award_XX', description: '用户奖励分表（按用户ID后两位）' }
]

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    // 二次确认
    await ElMessageBox.confirm(
      `即将删除用户 ${form.user_id} 的所有精灵任务数据（6个表），此操作不可恢复！确定要继续吗？`,
      '最终确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error',
        distinguishCancelAndClose: true
      }
    )

    submitting.value = true

    const res = await deleteTask({
      user_id: form.user_id
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '删除成功')

      // 显示结果
      resultData.value = res.data

      // 清空表单
      form.user_id = ''
      if (formRef.value) {
        formRef.value.resetFields()
      }
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    if (error === 'cancel' || error === 'close') {
      ElMessage.info('已取消操作')
    } else if (error !== false) {
      ElMessage.error('操作失败')
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
  resultData.value = null
}
</script>

<style scoped>
.del-task {
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

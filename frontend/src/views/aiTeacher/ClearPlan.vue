<template>
  <div class="clear-plan">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>清空学习计划</span>
          <el-tag type="danger">⚠️ 危险操作</el-tag>
        </div>
      </template>

      <!-- 危险操作警告 -->
      <el-alert type="error" :closable="false" style="margin-bottom: 20px">
        <template #title>
          <strong>🚨 危险操作警告</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li><strong>此操作将删除用户的所有AI外教学习计划数据</strong></li>
          <li>包含12个数据表的用户数据（学习记录、考试信息、统计数据等）</li>
          <li><strong style="color: #f56c6c">删除后无法恢复</strong></li>
          <li>请务必确认用户ID正确后再执行</li>
        </ul>
      </el-alert>

      <!-- 操作表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input
            v-model="form.user_id"
            placeholder="请输入要清空学习计划的用户ID"
            clearable
            style="width: 500px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="danger" :loading="submitting" @click="handleSubmit">
            确认清空
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 将要删除的表列表 -->
      <el-collapse style="margin-top: 20px">
        <el-collapse-item title="查看将要清空的数据表（12个表）" name="1">
          <el-table :data="tableList" stripe border max-height="300">
            <el-table-column type="index" label="序号" width="80" />
            <el-table-column prop="table" label="表名" show-overflow-tooltip />
            <el-table-column prop="description" label="说明" show-overflow-tooltip />
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 清空结果 -->
    <el-card v-if="resultData" class="result-card">
      <template #header>
        <div class="card-header">
          <span>清空结果</span>
          <el-tag :type="resultData.success ? 'success' : 'danger'">
            {{ resultData.success ? '清空成功' : '清空失败' }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border style="margin-bottom: 20px">
        <el-descriptions-item label="用户ID">
          {{ resultData.user_id }}
        </el-descriptions-item>
        <el-descriptions-item label="删除总数">
          <el-tag type="danger">{{ resultData.total_deleted }} 条</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="成功表数">
          <el-tag type="success">{{ resultData.success_count }} 个</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="失败表数">
          <el-tag type="warning">{{ resultData.failed_count }} 个</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">各表删除详情</el-divider>

      <el-table :data="resultData.deleted_tables" stripe border max-height="300">
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="table" label="表名" show-overflow-tooltip />
        <el-table-column prop="deleted_count" label="删除记录数" width="150">
          <template #default="{ row }">
            <el-tag type="info">{{ row.deleted_count }} 条</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="resultData.failed_tables && resultData.failed_tables.length > 0" style="margin-top: 20px">
        <el-divider content-position="left">失败表详情</el-divider>
        <el-table :data="resultData.failed_tables" stripe border max-height="200">
          <el-table-column type="index" label="序号" width="80" />
          <el-table-column prop="table" label="表名" width="200" />
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
import { clearStudyPlan } from '@/api/aiTeacher'

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

// 清空结果
const resultData = ref(null)

// 数据表列表
const tableList = [
  { table: 'user_info', description: '用户基础信息' },
  { table: 'user_lesson_consume_record', description: '课程消费记录' },
  { table: 'user_lesson_exam_info', description: '课程考试信息' },
  { table: 'user_report', description: '用户学习报告' },
  { table: 'user_test_analysis', description: '测试分析数据' },
  { table: 'user_statistics_gold_coin_log', description: '金币统计日志' },
  { table: 'user_week_statistics', description: '周统计数据' },
  { table: 'user_week_plan', description: '周学习计划' },
  { table: 'user_timetable_finish_record', description: '课表完成记录' },
  { table: 'user_statistics', description: '用户统计数据' },
  { table: 'user_timetable', description: '用户课表' },
  { table: 'user_update_log', description: '用户更新日志' }
]

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    // 二次确认
    await ElMessageBox.confirm(
      `即将清空用户 ${form.user_id} 的所有学习计划数据（12个表），此操作不可恢复！确定要继续吗？`,
      '最终确认',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'error',
        distinguishCancelAndClose: true
      }
    )

    submitting.value = true

    const res = await clearStudyPlan({
      user_id: form.user_id
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '清空成功')

      // 显示结果
      resultData.value = {
        ...res.data,
        success: true
      }

      // 清空表单
      form.user_id = ''
      if (formRef.value) {
        formRef.value.resetFields()
      }
    } else {
      ElMessage.error(res.msg || '清空失败')

      // 显示错误结果
      resultData.value = {
        user_id: form.user_id,
        success: false,
        total_deleted: 0,
        success_count: 0,
        failed_count: 0,
        deleted_tables: [],
        failed_tables: []
      }
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
.clear-plan {
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

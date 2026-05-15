<template>
  <div class="clear-plan-page">
    <el-card>
      <template #header>
        <span><strong>测试环境</strong>清除绘本学习计划</span>
      </template>
      <!-- 危险操作警告 -->
      <el-alert type="error" :closable="false" style="margin-bottom: 20px">
        <template #title>
          <strong>🚨 危险操作警告</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li>此操作将<strong>永久删除测试环境</strong>该用户的所有绘本学习数据</li>
          <li>删除范围包括: 用户信息、学习记录、统计数据、阅读计划等12个数据表</li>
          <li>同时会自动清除用户相关的Redis缓存</li>
          <li><strong style="color: #e6a23c;">删除后无法恢复，请谨慎操作！</strong></li>
        </ul>
      </el-alert>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户ID" prop="user_id">
          <HistoryInput
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            storage-key="pb-clear-plan_user_id"
            style="width: 300px" />
          <el-text type="info" size="small" style="margin-left: 10px;">
            输入需要清除绘本数据的用户ID
          </el-text>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="可选：记录清除原因"
            style="width: 500px" />
        </el-form-item>

        <el-form-item>
          <el-button type="danger" :loading="loading" @click="handleSubmit">
            清除学习计划
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 操作结果展示 -->
      <el-divider v-if="result" />

      <el-descriptions
        v-if="result"
        title="清除结果"
        :column="2"
        border>
        <el-descriptions-item label="用户ID">
          {{ result.user_id }}
        </el-descriptions-item>
        <el-descriptions-item label="操作状态">
          <el-tag type="success">成功</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="数据库删除" :span="2">
          共删除 <strong>{{ result.database.total_deleted }}</strong> 条记录
        </el-descriptions-item>
        <el-descriptions-item label="Redis缓存清理" :span="2">
          <div>
            总计删除 <strong>{{ result.redis.total_deleted }}</strong> 个键
            <div v-if="result.redis.nodes_result" style="margin-top: 8px; font-size: 12px;">
              <el-tag
                v-for="(count, node) in result.redis.nodes_result"
                :key="node"
                size="small"
                style="margin-right: 5px;">
                {{ node }}: {{ count }}个
              </el-tag>
            </div>
          </div>
        </el-descriptions-item>
      </el-descriptions>

      <!-- 详细删除信息 -->
      <el-collapse v-if="result && result.database.details" style="margin-top: 20px;">
        <el-collapse-item title="查看详细删除信息" name="1">
          <el-table :data="formatDetails(result.database.details)" border>
            <el-table-column prop="table" label="数据表" width="300" />
            <el-table-column prop="count" label="删除记录数" width="120" />
          </el-table>

          <el-divider v-if="result.redis.sample_keys.length > 0" />

          <div v-if="result.redis.sample_keys.length > 0">
            <div style="margin-bottom: 10px; font-weight: 500;">
              Redis键示例 (前10个):
            </div>
            <el-tag
              v-for="(key, index) in result.redis.sample_keys"
              :key="index"
              size="small"
              style="margin: 5px;">
              {{ key }}
            </el-tag>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { clearPicturebookPlan } from '@/api/picturebook'

const formRef = ref(null)
const loading = ref(false)
const result = ref(null)

const form = reactive({
  user_id: '',
  remark: ''
})

const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    // 二次确认
    await ElMessageBox.confirm(
      `确定要清除用户 ${form.user_id} 的绘本学习计划吗？此操作不可恢复！`,
      '危险操作确认',
      {
        confirmButtonText: '确定清除',
        cancelButtonText: '取消',
        type: 'error',
        confirmButtonClass: 'el-button--danger'
      }
    )

    loading.value = true
    result.value = null

    const response = await clearPicturebookPlan({
      user_id: form.user_id
    })

    if (response.code === '10000') {
      ElMessage.success('绘本学习计划清除成功')
      result.value = response.data

      // 记录操作日志
      console.log('[绘本清理] 操作成功:', {
        user_id: form.user_id,
        remark: form.remark,
        timestamp: new Date().toLocaleString(),
        result: response.data
      })
    } else {
      ElMessage.error(`清除失败: ${response.message}`)
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('[绘本清理] 操作失败:', error)
      ElMessage.error(`清除失败: ${error.message || error}`)
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  form.user_id = ''
  form.remark = ''
  result.value = null
  formRef.value?.resetFields()
}

// 格式化详细信息为表格数据
const formatDetails = (details) => {
  return Object.entries(details).map(([table, count]) => ({
    table,
    count
  }))
}
</script>

<style scoped>
.clear-plan-page {
  padding: 20px;
}

.el-form-item {
  margin-bottom: 22px;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
}

:deep(.el-collapse-item__header) {
  font-weight: 500;
}
</style>

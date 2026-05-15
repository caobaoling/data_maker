<template>
  <div class="add-wealth">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>添加用户财富</span>
          <el-tag type="info">为用户添加各类财富资产</el-tag>
        </div>
      </template>

      <!-- 添加表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <HistoryInput
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            storage-key="add-wealth_user_id"
            style="width: 400px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </HistoryInput>
        </el-form-item>

        <el-form-item label="财富类型" prop="sku_type">
          <el-select
            v-model="form.sku_type"
            placeholder="请选择财富类型"
            style="width: 400px"
            filterable>
            <el-option
              v-for="item in wealthTypes"
              :key="item.sku_type"
              :label="`${item.name} (${item.sku_type})`"
              :value="item.sku_type">
              <span style="float: left">{{ item.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                SKU: {{ item.sku_id }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数量" prop="count">
          <el-input-number
            v-model="form.count"
            :min="1"
            :max="10000"
            :step="100"
            style="width: 400px" />
          <span style="margin-left: 10px; color: #909399">默认100</span>
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
            添加财富
          </el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="info" @click="handleQuery">查询财富</el-button>
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
        <el-descriptions-item label="总数量">
          <el-tag type="info" size="large">{{ queryResult.total_count }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="有效数量">
          <el-tag type="warning" size="large">{{ getValidCount() }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="记录数">
          {{ queryResult.assets.length }} 条
        </el-descriptions-item>
        <el-descriptions-item label="有效记录">
          {{ getValidRecordsCount() }} 条
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">财富明细</el-divider>

      <el-table :data="queryResult.assets" stripe border max-height="400">
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="wealth_name" label="财富类型" width="120">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.wealth_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sku_type" label="SKU类型" width="150" show-overflow-tooltip />
        <el-table-column prop="count" label="数量" width="100">
          <template #default="{ row }">
            <el-tag type="success">{{ row.count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row)">{{ getStatusText(row) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="valid_start" label="生效日期" width="120" />
        <el-table-column prop="valid_end" label="到期日期" width="120" />
        <el-table-column prop="days" label="有效天数" width="100" />
        <el-table-column prop="id" label="记录ID" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { addWealth, queryWealth, getWealthTypes } from '@/api/user'

// 表单引用
const formRef = ref(null)

// 财富类型列表
const wealthTypes = ref([])

// 表单数据
const form = reactive({
  user_id: '',
  sku_type: '',
  count: 100,
  days: 300
})

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  sku_type: [
    { required: true, message: '请选择财富类型', trigger: 'change' }
  ],
  count: [
    { required: true, message: '请输入数量', trigger: 'blur' }
  ],
  days: [
    { required: true, message: '请输入有效天数', trigger: 'blur' }
  ]
}

// 提交状态
const submitting = ref(false)

// 查询结果
const queryResult = ref(null)

// 加载财富类型
const loadWealthTypes = async () => {
  try {
    const res = await getWealthTypes()
    if (res.code === '0') {
      wealthTypes.value = res.data
    } else {
      ElMessage.error(res.msg || '加载财富类型失败')
    }
  } catch (error) {
    ElMessage.error('加载财富类型失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true

    const res = await addWealth({
      user_id: form.user_id,
      sku_type: form.sku_type,
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

// 查询财富
const handleQuery = async () => {
  if (!form.user_id) {
    ElMessage.warning('请先输入用户ID')
    return
  }

  try {
    const res = await queryWealth({
      user_id: form.user_id
    })

    if (res.code === '0') {
      // 对查询结果按状态排序：有效 > 未生效 > 已过期
      const sortedAssets = res.data.assets.sort((a, b) => {
        const statusA = getStatusValue(a)
        const statusB = getStatusValue(b)
        return statusA - statusB
      })

      queryResult.value = {
        ...res.data,
        assets: sortedAssets
      }
      ElMessage.success('查询成功')
    } else {
      ElMessage.error(res.msg || '查询失败')
    }
  } catch (error) {
    ElMessage.error('查询失败')
  }
}

// 获取状态排序值（用于排序）
const getStatusValue = (row) => {
  // 优先检查数据库状态字段
  if (row.status === 'disable') {
    return 2  // 未启用 - 排在有效之后
  }
  if (row.status === 'refund') {
    return 5  // 已退款 - 优先级最低
  }

  // 如果状态是enable或expired，再根据日期判断
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const startDate = new Date(row.valid_start)
  startDate.setHours(0, 0, 0, 0)

  const endDate = new Date(row.valid_end)
  endDate.setHours(23, 59, 59, 999)

  if (today >= startDate && today <= endDate) {
    return 1  // 有效 - 优先级最高
  } else if (today < startDate) {
    return 3  // 未生效 - 优先级中等
  } else {
    return 4  // 已过期 - 优先级较低
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
  // 优先检查数据库状态字段
  if (row.status === 'disable') {
    return '未启用'
  }
  if (row.status === 'expired') {
    return '已过期'
  }
  if (row.status === 'refund') {
    return '已退款'
  }

  // 如果状态是enable，再根据日期判断
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
  // 优先检查数据库状态字段
  if (row.status === 'disable') {
    return 'warning'  // 未启用 - 橙色
  }
  if (row.status === 'expired' || row.status === 'refund') {
    return 'danger'   // 已过期/已退款 - 红色
  }

  // 如果状态是enable，再根据日期判断
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

// 计算有效数量总和
const getValidCount = () => {
  if (!queryResult.value || !queryResult.value.assets) return 0

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return queryResult.value.assets.reduce((total, row) => {
    const startDate = new Date(row.valid_start)
    startDate.setHours(0, 0, 0, 0)

    const endDate = new Date(row.valid_end)
    endDate.setHours(23, 59, 59, 999)

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

    return today >= startDate && today <= endDate
  }).length
}

// 组件挂载时加载财富类型
onMounted(() => {
  loadWealthTypes()
})
</script>

<style scoped>
.add-wealth {
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

<template>
  <div class="release-risk">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>解除高风险</strong>用户设备登录限制</span>
          <el-tag type="danger">线上环境</el-tag>
        </div>
      </template>

      <el-alert
        title="警告：此功能操作线上环境数据，请谨慎使用！"
        type="warning"
        :closable="false"
        show-icon
        style="margin-bottom: 20px;" />

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="环境选择" prop="env_type">
          <el-radio-group v-model="form.env_type">
            <el-radio label="domestic">境内环境</el-radio>
            <el-radio label="overseas">境外环境</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="学员ID" prop="stu_id">
          <HistoryInput
            v-model="form.stu_id"
            placeholder="请输入学员ID"
            clearable
            storage-key="release-risk_stu_id"
            style="width: 300px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </HistoryInput>
        </el-form-item>

        <el-form-item label="风险类型" prop="risk_type">
          <el-radio-group v-model="form.risk_type">
            <el-radio label="1">设备</el-radio>
            <el-radio label="2">用户</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="风险项ID" prop="risk_item">
          <HistoryInput
            v-model="form.risk_item"
            placeholder="请输入设备ID或用户ID，默认使用学员ID"
            clearable
            storage-key="release-risk_risk_item"
            style="width: 300px">
          </HistoryInput>
          <div class="form-tip">如不填写，默认使用学员ID</div>
        </el-form-item>

        <el-form-item label="操作" prop="action_type">
          <el-checkbox-group v-model="form.action_type">
            <el-checkbox label="release">解除高风险</el-checkbox>
            <el-checkbox label="whitelist">添加白名单</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            执行操作
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 结果展示 -->
    <el-card v-if="result" class="result-card">
      <template #header>
        <div class="card-header">
          <span>操作结果</span>
          <el-tag :type="result.success ? 'success' : 'danger'">
            {{ result.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <div v-if="result.success" class="success-result">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="学员ID">{{ result.stu_id }}</el-descriptions-item>
          <el-descriptions-item label="风险类型">{{ result.risk_type === '1' ? '设备' : '用户' }}</el-descriptions-item>
          <el-descriptions-item label="环境">{{ result.env_type === 'domestic' ? '境内环境' : '境外环境' }}</el-descriptions-item>
          <el-descriptions-item label="风险项ID">{{ result.risk_item }}</el-descriptions-item>
          <el-descriptions-item label="执行操作">
            <el-tag v-if="result.release_success" type="success" class="action-tag">解除高风险</el-tag>
            <el-tag v-if="result.whitelist_success" type="success" class="action-tag">添加白名单</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <el-alert
        v-else
        :title="result.message || '操作失败'"
        type="error"
        :closable="false"
        show-icon />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { releaseRisk, addWhitelist } from '@/api/risk'

const formRef = ref(null)

const form = reactive({
  env_type: 'domestic',
  stu_id: '',
  risk_type: '2',
  risk_item: '',
  action_type: ['release', 'whitelist']
})

const rules = {
  env_type: [
    { required: true, message: '请选择环境', trigger: 'change' }
  ],
  stu_id: [
    { required: true, message: '请输入学员ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '学员ID必须是数字', trigger: 'blur' }
  ],
  risk_type: [
    { required: true, message: '请选择风险类型', trigger: 'change' }
  ],
  action_type: [
    { required: true, message: '请至少选择一项操作', trigger: 'change' }
  ]
}

const loading = ref(false)
const result = ref(null)

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    if (form.action_type.length === 0) {
      ElMessage.error('请至少选择一项操作')
      return
    }

    loading.value = true
    result.value = null

    const riskItem = form.risk_item || form.stu_id
    let releaseSuccess = false
    let whitelistSuccess = false
    let errorMsg = ''

    // 解除高风险
    if (form.action_type.includes('release')) {
      const releaseRes = await releaseRisk({
        env_type: form.env_type,
        stu_id: form.stu_id,
        risk_type: form.risk_type,
        risk_item: riskItem
      })
      if (releaseRes.code === '0') {
        releaseSuccess = true
      } else {
        errorMsg = releaseRes.msg || '解除高风险失败'
      }
    }

    // 添加白名单
    if (form.action_type.includes('whitelist')) {
      const whitelistRes = await addWhitelist({
        env_type: form.env_type,
        stu_id: form.stu_id,
        risk_type: form.risk_type,
        risk_item: riskItem
      })
      if (whitelistRes.code === '0') {
        whitelistSuccess = true
      } else {
        errorMsg = errorMsg || whitelistRes.msg || '添加白名单失败'
      }
    }

    if (releaseSuccess || whitelistSuccess) {
      result.value = {
        success: true,
        env_type: form.env_type,
        stu_id: form.stu_id,
        risk_type: form.risk_type,
        risk_item: riskItem,
        release_success: releaseSuccess,
        whitelist_success: whitelistSuccess
      }
      ElMessage.success('操作执行成功')
    } else {
      result.value = {
        success: false,
        message: errorMsg || '操作失败'
      }
      ElMessage.error(errorMsg || '操作失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  result.value = null
}
</script>

<style scoped>
.release-risk {
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

.success-result {
  padding: 10px 0;
}

.action-tag {
  margin-right: 10px;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>

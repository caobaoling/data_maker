<template>
  <div class="user-manage">
    <!-- 环境提示 -->
    <el-card class="env-card">
      <el-tag type="warning" class="env-tag"><strong>当前：测试环境（admin）</strong></el-tag>
    </el-card>

    <!-- 获取手机号 -->
    <el-card class="action-card">
      <template #header>
        <span><strong>获取手机号</strong>（通过用户ID）</span>
      </template>
      <el-form :model="mobileForm" label-width="100px" @submit.prevent>
        <el-form-item label="用户ID">
          <HistoryInput v-model="mobileForm.user_id" placeholder="请输入用户ID" clearable storage-key="user-manage_mobile_user_id" style="width: 300px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="mobileLoading" @click="handleGetMobile">获取手机号</el-button>
        </el-form-item>
      </el-form>
      <div v-if="mobileResult" class="result-alert">
        <el-alert
          v-if="!mobileResult.success"
          :title="mobileResult.msg"
          type="error"
          show-icon
          :closable="false"
        />
        <div v-else class="mobile-result">
          <el-icon class="mobile-icon"><Phone /></el-icon>
          <span class="mobile-label">手机号：</span>
          <span class="mobile-value">{{ mobileResult.mobile }}</span>
          <el-button text type="primary" size="small" @click="copyMobile(mobileResult.mobile)">复制</el-button>
        </div>
      </div>
    </el-card>

    <!-- 打海外标签 -->
    <el-card class="action-card">
      <template #header>
        <span><strong>打海外标签</strong>（通过用户ID）</span>
      </template>
      <el-form :model="labelForm" label-width="100px" @submit.prevent>
        <el-form-item label="用户ID">
          <HistoryInput v-model="labelForm.user_id" placeholder="请输入用户ID" clearable storage-key="user-manage_label_user_id" style="width: 300px" />
        </el-form-item>
        <el-form-item label="国家代码">
          <HistoryInput v-model="labelForm.country_code" placeholder="默认886（台湾）" clearable storage-key="user-manage_country_code" style="width: 200px" />
        </el-form-item>
        <el-form-item>
          <el-button type="warning" :loading="labelLoading" @click="handleAddLabel">打海外标签</el-button>
        </el-form-item>
      </el-form>
      <el-alert
        v-if="labelResult"
        :title="labelResult.msg"
        :description="labelResult.raw"
        :type="labelResult.success ? 'success' : 'error'"
        show-icon
        :closable="false"
        class="result-alert"
      />
    </el-card>

    <!-- 解锁账户 -->
    <el-card class="action-card">
      <template #header>
        <span><strong>自动解锁账户</strong>（通过用户ID）</span>
      </template>
      <el-form :model="unlockForm" label-width="100px" @submit.prevent>
        <el-form-item label="用户ID">
          <HistoryInput v-model="unlockForm.username" placeholder="请输入用户ID" clearable storage-key="user-manage_unlock_username" style="width: 300px" />
        </el-form-item>
        <el-form-item label="用户区域">
          <el-radio-group v-model="unlockForm.region">
            <el-radio value="domestic">境内（51suyang.cn）</el-radio>
            <el-radio value="overseas">境外（51talk.com）</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="danger" :loading="unlockLoading" @click="handleUnlock">解锁账户</el-button>
        </el-form-item>
      </el-form>
      <el-alert
        v-if="unlockResult"
        :title="unlockResult.msg"
        :type="unlockResult.success ? 'success' : 'error'"
        show-icon
        :closable="false"
        class="result-alert"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Phone } from '@element-plus/icons-vue'
import { getMobile, addOverseasLabel, unlockAccount } from '@/api/user'

const copyMobile = (mobile) => {
  navigator.clipboard.writeText(mobile).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

// 获取手机号
const mobileForm = reactive({ user_id: '' })
const mobileLoading = ref(false)
const mobileResult = ref(null)

const handleGetMobile = async () => {
  if (!mobileForm.user_id.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }
  mobileLoading.value = true
  mobileResult.value = null
  try {
    const res = await getMobile({ user_id: mobileForm.user_id.trim(), env: 'test' })
    if (res.code === '0') {
      mobileResult.value = { success: true, msg: '获取成功', mobile: res.data?.mobile, raw: res.data?.raw }
    } else {
      mobileResult.value = { success: false, msg: res.msg || '获取失败', raw: '' }
    }
  } catch (e) {
    mobileResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    mobileLoading.value = false
  }
}

// 打海外标签
const labelForm = reactive({ user_id: '', country_code: '886' })
const labelLoading = ref(false)
const labelResult = ref(null)

const handleAddLabel = async () => {
  if (!labelForm.user_id.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }
  labelLoading.value = true
  labelResult.value = null
  try {
    const res = await addOverseasLabel({ user_id: labelForm.user_id.trim(), country_code: labelForm.country_code || '886', env: 'test' })
    if (res.code === '0') {
      let detail = res.data?.raw || ''
      let success = true
      try {
        const parsed = JSON.parse(res.data?.raw)
        detail = parsed.info || parsed.message || JSON.stringify(parsed)
        success = parsed.status === 1 || parsed.status === 0
      } catch (_) {}
      labelResult.value = { success, msg: success ? '操作成功' : '操作失败', raw: detail }
    } else {
      labelResult.value = { success: false, msg: res.msg || '操作失败', raw: '' }
    }
  } catch (e) {
    labelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    labelLoading.value = false
  }
}

// 解锁账户
const unlockForm = reactive({ username: '', region: 'domestic' })
const unlockLoading = ref(false)
const unlockResult = ref(null)

const handleUnlock = async () => {
  if (!unlockForm.username.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }
  unlockLoading.value = true
  unlockResult.value = null
  try {
    const res = await unlockAccount({ username: unlockForm.username.trim(), region: unlockForm.region, env: 'test' })
    if (res.code === '0') {
      let success = true
      try {
        const parsed = JSON.parse(res.data?.raw)
        success = parsed.status === 0
      } catch (_) {}
      unlockResult.value = { success, msg: success ? '解锁成功' : '解锁失败' }
    } else {
      unlockResult.value = { success: false, msg: res.msg || '解锁失败' }
    }
  } catch (e) {
    unlockResult.value = { success: false, msg: '请求异常' }
  } finally {
    unlockLoading.value = false
  }
}
</script>

<style scoped>
.user-manage {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.env-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
}

.env-tag {
  font-size: 13px;
}

.action-card {
  width: 100%;
}

.result-alert {
  margin-top: 12px;
}

.mobile-result {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: #f0f9eb;
  border: 1px solid #b3e19d;
  border-radius: 4px;
}

.mobile-icon {
  color: #67c23a;
  font-size: 16px;
}

.mobile-label {
  color: #606266;
  font-size: 14px;
}

.mobile-value {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  letter-spacing: 1px;
}
</style>

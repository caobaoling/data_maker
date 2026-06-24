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

    <!-- 海外标签管理 -->
    <el-card class="action-card">
      <template #header>
        <span><strong>海外标签管理</strong>（通过用户ID）</span>
      </template>
      <el-form :model="labelForm" label-width="100px" @submit.prevent>
        <el-form-item label="用户ID">
          <HistoryInput v-model="labelForm.user_id" placeholder="请输入用户ID" clearable storage-key="user-manage_label_user_id" style="width: 300px" />
        </el-form-item>
        <el-form-item>
          <el-button :loading="queryLabelLoading" @click="handleQueryLabel">查询海外标签</el-button>
          <el-button type="warning" :loading="labelLoading" @click="handleAddLabel" style="margin-left: 12px;">添加海外标签</el-button>
          <el-button type="danger" :loading="deleteLabelLoading" @click="handleDeleteLabel" style="margin-left: 12px;">删除海外标签</el-button>
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

    <!-- Cocos标签管理 -->
    <el-card class="action-card">
      <template #header>
        <span><strong>Cocos标签管理</strong>（通过用户ID）</span>
      </template>
      <el-form :model="cocosLabelForm" label-width="100px" @submit.prevent>
        <el-form-item label="用户ID">
          <HistoryInput v-model="cocosLabelForm.user_id" placeholder="请输入用户ID" clearable storage-key="user-manage_cocos_label_user_id" style="width: 300px" />
        </el-form-item>
        <el-form-item>
          <el-button :loading="queryCocosLabelLoading" @click="handleQueryCocosLabel">查询Cocos标签</el-button>
          <el-button type="warning" :loading="cocosLabelLoading" @click="handleAddCocosLabel" style="margin-left: 12px;">添加Cocos标签</el-button>
          <el-button type="danger" :loading="deleteCocosLabelLoading" @click="handleDeleteCocosLabel" style="margin-left: 12px;">删除Cocos标签</el-button>
        </el-form-item>
      </el-form>
      <el-alert
        v-if="cocosLabelResult"
        :title="cocosLabelResult.msg"
        :description="cocosLabelResult.raw"
        :type="cocosLabelResult.success ? 'success' : 'error'"
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
import { getMobile, addOverseasLabel, queryOverseasLabel, deleteOverseasLabel, queryCocosLabel, addCocosLabel, deleteCocosLabel, unlockAccount } from '@/api/user'

const copyMobile = (mobile) => {
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(mobile).then(() => {
      ElMessage.success('已复制到剪贴板')
    })
  } else {
    const textarea = document.createElement('textarea')
    textarea.value = mobile
    textarea.style.position = 'fixed'
    textarea.style.opacity = '0'
    document.body.appendChild(textarea)
    textarea.focus()
    textarea.select()
    try {
      document.execCommand('copy')
      ElMessage.success('已复制到剪贴板')
    } finally {
      document.body.removeChild(textarea)
    }
  }
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

// 海外标签管理
const labelForm = reactive({ user_id: '', country_code: '886' })
const labelLoading = ref(false)
const queryLabelLoading = ref(false)
const deleteLabelLoading = ref(false)
const labelResult = ref(null)

// 将后端解析好的单个 type 结果格式化为可读文本
// action: 'query' | 'add' | 'delete'
const formatLabelItem = (item, labelType, action) => {
  if (!item) return `${labelType}: 无响应`
  if (action === 'add') {
    // 第一个 code：10000=添加前已存在，60024=添加前不存在（本次已添加）
    return `${labelType}: ${item.has_label ? '已存在' : '已添加'}`
  }
  if (action === 'delete') {
    // 第一个 code：10000=删除前有标签（本次已删除），60024=删除前无标签
    return `${labelType}: ${item.has_label ? '已删除' : '不存在'}`
  }
  return `${labelType}: ${item.has_label ? '存在' : '不存在'}`
}

const handleQueryLabel = async () => {
  if (!labelForm.user_id.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }
  queryLabelLoading.value = true
  labelResult.value = null
  try {
    const res = await queryOverseasLabel({ user_id: labelForm.user_id.trim() })
    if (res.code === '0') {
      const lines = [
        formatLabelItem(res.data?.overseas, 'overseas'),
        formatLabelItem(res.data?.global, 'global')
      ]
      const hasAny = res.data?.overseas?.has_label || res.data?.global?.has_label
      labelResult.value = { success: true, msg: `查询结果：标签${hasAny ? '存在' : '不存在'}`, raw: lines.join('\n') }
    } else {
      labelResult.value = { success: false, msg: res.msg || '查询失败', raw: '' }
    }
  } catch (e) {
    labelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    queryLabelLoading.value = false
  }
}

const handleAddLabel = async () => {
  if (!labelForm.user_id.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }
  labelLoading.value = true
  labelResult.value = null
  try {
    const res = await addOverseasLabel({ user_id: labelForm.user_id.trim() })
    if (res.code === '0') {
      const lines = [
        formatLabelItem(res.data?.overseas, 'overseas', 'add'),
        formatLabelItem(res.data?.global, 'global', 'add')
      ]
      labelResult.value = { success: true, msg: '添加成功', raw: lines.join('\n') }
    } else {
      labelResult.value = { success: false, msg: res.msg || '操作失败', raw: '' }
    }
  } catch (e) {
    labelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    labelLoading.value = false
  }
}

const handleDeleteLabel = async () => {
  if (!labelForm.user_id.trim()) {
    ElMessage.warning('请输入用户ID')
    return
  }
  deleteLabelLoading.value = true
  labelResult.value = null
  try {
    const res = await deleteOverseasLabel({ user_id: labelForm.user_id.trim() })
    if (res.code === '0') {
      const lines = [
        formatLabelItem(res.data?.overseas, 'overseas', 'delete'),
        formatLabelItem(res.data?.global, 'global', 'delete')
      ]
      labelResult.value = { success: true, msg: '删除成功', raw: lines.join('\n') }
    } else {
      labelResult.value = { success: false, msg: res.msg || '操作失败', raw: '' }
    }
  } catch (e) {
    labelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    deleteLabelLoading.value = false
  }
}

// Cocos标签管理
const cocosLabelForm = reactive({ user_id: '' })
const cocosLabelLoading = ref(false)
const queryCocosLabelLoading = ref(false)
const deleteCocosLabelLoading = ref(false)
const cocosLabelResult = ref(null)

const formatCocosLabelItem = (item, action) => {
  if (!item) return 'cocos: 无响应'
  if (action === 'add') return `cocos: ${item.has_label ? '已存在' : '已添加'}`
  if (action === 'delete') return `cocos: ${item.has_label ? '已删除' : '不存在'}`
  return `cocos: ${item.has_label ? '存在' : '不存在'}`
}

const handleQueryCocosLabel = async () => {
  if (!cocosLabelForm.user_id.trim()) { ElMessage.warning('请输入用户ID'); return }
  queryCocosLabelLoading.value = true
  cocosLabelResult.value = null
  try {
    const res = await queryCocosLabel({ user_id: cocosLabelForm.user_id.trim() })
    if (res.code === '0') {
      const hasAny = res.data?.cocos?.has_label
      cocosLabelResult.value = { success: true, msg: `查询结果：标签${hasAny ? '存在' : '不存在'}`, raw: formatCocosLabelItem(res.data?.cocos, 'query') }
    } else {
      cocosLabelResult.value = { success: false, msg: res.msg || '查询失败', raw: '' }
    }
  } catch (e) {
    cocosLabelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    queryCocosLabelLoading.value = false
  }
}

const handleAddCocosLabel = async () => {
  if (!cocosLabelForm.user_id.trim()) { ElMessage.warning('请输入用户ID'); return }
  cocosLabelLoading.value = true
  cocosLabelResult.value = null
  try {
    const res = await addCocosLabel({ user_id: cocosLabelForm.user_id.trim() })
    if (res.code === '0') {
      cocosLabelResult.value = { success: true, msg: '添加成功', raw: formatCocosLabelItem(res.data?.cocos, 'add') }
    } else {
      cocosLabelResult.value = { success: false, msg: res.msg || '操作失败', raw: '' }
    }
  } catch (e) {
    cocosLabelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    cocosLabelLoading.value = false
  }
}

const handleDeleteCocosLabel = async () => {
  if (!cocosLabelForm.user_id.trim()) { ElMessage.warning('请输入用户ID'); return }
  deleteCocosLabelLoading.value = true
  cocosLabelResult.value = null
  try {
    const res = await deleteCocosLabel({ user_id: cocosLabelForm.user_id.trim() })
    if (res.code === '0') {
      cocosLabelResult.value = { success: true, msg: '删除成功', raw: formatCocosLabelItem(res.data?.cocos, 'delete') }
    } else {
      cocosLabelResult.value = { success: false, msg: res.msg || '操作失败', raw: '' }
    }
  } catch (e) {
    cocosLabelResult.value = { success: false, msg: '请求异常', raw: String(e) }
  } finally {
    deleteCocosLabelLoading.value = false
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

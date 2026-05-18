<template>
  <div class="tms-page">
    <el-card>
      <template #header>
        <span><strong>{{ title }}</strong></span>
      </template>

      <div class="launch-area">
        <p class="desc">点击下方按钮，将自动完成 TMS 登录并打开目标页面。</p>
        <el-button
          type="primary"
          size="large"
          :loading="loading"
          :icon="Link"
          @click="handleOpen">
          {{ loading ? '正在登录 TMS...' : '打开页面' }}
        </el-button>
        <el-alert
          v-if="errorMsg"
          :title="errorMsg"
          type="error"
          show-icon
          :closable="false"
          style="margin-top: 16px"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Link } from '@element-plus/icons-vue'
import { getTmsSsoUrl } from '@/api/teacher'

const route = useRoute()
const loading = ref(false)
const errorMsg = ref('')

const targetUrl = computed(() => route.meta.tmsUrl || '')
const title = computed(() => route.meta.title || 'TMS 页面')

const handleOpen = async () => {
  if (!targetUrl.value) {
    ElMessage.error('未配置目标 URL')
    return
  }
  loading.value = true
  errorMsg.value = ''
  try {
    const res = await getTmsSsoUrl({ target_url: targetUrl.value })
    if (res.code !== '0') {
      errorMsg.value = res.msg || '获取登录链接失败'
      return
    }
    const { sso_url, target_url: tUrl } = res.data
    // 先在新窗口访问 SSO URL 建立 TMS session，短暂停留后跳转目标页
    const win = window.open(sso_url, '_blank')
    if (!win) {
      errorMsg.value = '弹窗被拦截，请允许本站弹出窗口后重试'
      return
    }
    // 等待 SSO 完成后跳转目标页（SSO 本身是 302 很快，1.5s 足够）
    setTimeout(() => {
      win.location.href = tUrl
    }, 1500)
    ElMessage.success('已打开，请在新窗口查看')
  } catch (e) {
    errorMsg.value = '请求异常：' + String(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.tms-page {
  max-width: 600px;
}

.launch-area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

.desc {
  color: #606266;
  font-size: 14px;
  margin: 0;
}
</style>

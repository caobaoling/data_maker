<template>
  <div class="add-star-placeholder">
    <el-empty description="功能开发中，敬请期待">
      <template #image>
        <el-icon :size="100" color="#409eff">
          <Tools />
        </el-icon>
      </template>

      <template #description>
        <h2>🚧 功能开发中，敬请期待 🚧</h2>
        <el-space direction="vertical" alignment="start" style="margin-top: 20px">
          <p>本功能将支持:</p>
          <ul style="text-align: left; padding-left: 20px;">
            <li>✓ 为课程添加星星评价 (1-5星)</li>
            <li>✓ 触发精灵任务奖励</li>
            <li>✓ 自动获取认证Token</li>
          </ul>
          <p style="color: #909399">预计上线时间: 第二期</p>
        </el-space>
      </template>

      <el-button type="primary" @click="goToList">
        返回预约列表
      </el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { Tools } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToList = () => {
  router.push('/appoint/list')
}
</script>

<style scoped>
.add-star-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}
</style>

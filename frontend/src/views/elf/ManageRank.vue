<template>
  <div class="manage-rank">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>管理排行榜</span>
          <el-tag type="warning">清理上周数据并重置状态</el-tag>
        </div>
      </template>

      <!-- 功能说明 -->
      <el-alert type="info" :closable="false" style="margin-bottom: 20px">
        <template #title>
          <strong>功能说明</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li>自动计算上周的时间键（格式: YYYY-wWW）</li>
          <li>删除上周的排行榜数据（3个表）</li>
          <li>重置机器人使用状态为可用</li>
          <li>重置用户等级使用标志为可用</li>
        </ul>
      </el-alert>

      <!-- 执行按钮 -->
      <div style="margin-bottom: 20px">
        <el-button type="primary" size="large" :loading="submitting" @click="handleExecute">
          执行排行榜管理
        </el-button>
      </div>

      <!-- 操作详情 -->
      <el-collapse>
        <el-collapse-item title="查看将要执行的操作" name="1">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="操作1">
              删除 user_rank_round 表的上周数据
            </el-descriptions-item>
            <el-descriptions-item label="操作2">
              删除 rank_round 表的上周数据
            </el-descriptions-item>
            <el-descriptions-item label="操作3">
              删除 rank_round_reward 表的上周数据
            </el-descriptions-item>
            <el-descriptions-item label="操作4">
              重置 robot_rank.use_status = 0
            </el-descriptions-item>
            <el-descriptions-item label="操作5">
              重置 user_rank_level.use_flag = 0, del_flag = 0
            </el-descriptions-item>
          </el-descriptions>
        </el-collapse-item>
      </el-collapse>
    </el-card>

    <!-- 执行结果 -->
    <el-card v-if="resultData" class="result-card">
      <template #header>
        <div class="card-header">
          <span>执行结果</span>
          <el-tag type="success">执行成功</el-tag>
        </div>
      </template>

      <el-result icon="success" title="排行榜管理成功" :sub-title="`时间键: ${resultData.time_key}`">
        <template #extra>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="时间键">
              <el-tag type="primary" size="large">{{ resultData.time_key }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </template>
      </el-result>

      <el-divider content-position="left">执行的操作</el-divider>

      <el-timeline>
        <el-timeline-item
          v-for="(operation, index) in resultData.operations"
          :key="index"
          type="success"
          :timestamp="`操作 ${index + 1}`">
          {{ operation }}
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 操作历史 -->
    <el-card v-if="historyList.length > 0" class="history-card">
      <template #header>
        <div class="card-header">
          <span>操作历史</span>
          <el-button text @click="handleClearHistory">清空记录</el-button>
        </div>
      </template>

      <el-timeline>
        <el-timeline-item
          v-for="(item, index) in historyList"
          :key="index"
          :timestamp="item.timestamp"
          :type="item.success ? 'success' : 'danger'"
          placement="top">
          <el-card>
            <div>
              <el-tag :type="item.success ? 'success' : 'danger'" size="small">
                {{ item.success ? '执行成功' : '执行失败' }}
              </el-tag>
              <span style="margin-left: 10px">时间键: {{ item.time_key }}</span>
            </div>
            <div v-if="item.message" style="margin-top: 5px; color: #909399; font-size: 12px">
              {{ item.message }}
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { manageRank } from '@/api/elf'

// 提交状态
const submitting = ref(false)

// 执行结果
const resultData = ref(null)

// 操作历史
const historyList = ref([])

// 执行排行榜管理
const handleExecute = async () => {
  try {
    // 确认操作
    await ElMessageBox.confirm(
      '即将删除上周的排行榜数据并重置机器人和用户状态，确定要继续吗？',
      '确认操作',
      {
        confirmButtonText: '确定执行',
        cancelButtonText: '取消',
        type: 'warning',
        distinguishCancelAndClose: true
      }
    )

    submitting.value = true

    const res = await manageRank({})

    if (res.code === '0') {
      ElMessage.success(res.msg || '执行成功')

      // 显示结果
      resultData.value = res.data

      // 添加到历史记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        time_key: res.data.time_key,
        success: true,
        message: res.msg
      })
    } else {
      ElMessage.error(res.msg || '执行失败')

      // 添加失败记录
      historyList.value.unshift({
        timestamp: new Date().toLocaleString('zh-CN'),
        time_key: '未知',
        success: false,
        message: res.msg
      })
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

// 清空历史记录
const handleClearHistory = () => {
  historyList.value = []
  ElMessage.success('已清空历史记录')
}
</script>

<style scoped>
.manage-rank {
  padding: 0;
}

.form-card {
  margin-bottom: 20px;
}

.result-card {
  margin-bottom: 20px;
}

.history-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

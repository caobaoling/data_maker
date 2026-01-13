<template>
  <div class="add-appoint-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>添加课程预约</span>
          <el-button text @click="resetForm">重置表单</el-button>
        </div>
      </template>

      <el-form :model="form" label-width="120px">
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>

        <el-form-item label="课程类型" required>
          <el-radio-group v-model="form.courseType" @change="onCourseTypeChange">
            <el-radio label="31">普通话</el-radio>
            <el-radio label="1">英语</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="学生ID" required>
          <el-input v-model="form.stuId" placeholder="请输入学生ID" />
        </el-form-item>

        <el-form-item label="教师ID" required>
          <el-input v-model="form.teacherId" placeholder="请填写数字">
            <template #append>只能填写数字</template>
          </el-input>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            💡 提示: 请手动输入教师ID,只能填写数字
          </div>
        </el-form-item>

        <!-- 时间设置 -->
        <el-divider content-position="left">时间设置</el-divider>

        <el-form-item label="开始时间" required>
          <el-date-picker
            v-model="form.startTime"
            type="datetime"
            placeholder="选择日期时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss" />
        </el-form-item>

        <el-form-item label="结束时间">
          <el-input :model-value="endTime" disabled />
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">(自动计算)</div>
        </el-form-item>

        <el-form-item label="时间编号">
          <el-input :model-value="dateTime" disabled />
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">(自动生成)</div>
        </el-form-item>

        <!-- 课程信息 -->
        <el-divider content-position="left">课程信息</el-divider>

        <el-form-item label="课程性质">
          <el-radio-group v-model="form.usePoint">
            <el-radio label="buy">付费课(buy)</el-radio>
            <el-radio label="free">体验课(free)</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="教材选择">
          <el-space direction="vertical" style="width: 100%">
            <el-input v-model="form.courseId" placeholder="course_id">
              <template #prepend>course_id</template>
            </el-input>
            <el-input v-model="form.courseTopId" placeholder="course_top_id">
              <template #prepend>course_top_id</template>
            </el-input>
            <el-input v-model="form.courseSubId" placeholder="course_sub_id">
              <template #prepend>course_sub_id</template>
            </el-input>
            <div style="color: #909399; font-size: 12px;">
              💡 提示: 当前使用默认教材ID，可手动修改
            </div>
          </el-space>
        </el-form-item>

        <!-- 其他设置 -->
        <el-divider content-position="left">其他设置</el-divider>

        <el-form-item label="预约状态">
          <el-select v-model="form.status">
            <el-option label="正常(on)" value="on" />
            <el-option label="取消(cancel)" value="cancel" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注信息">
          <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="选填" />
        </el-form-item>

        <!-- 参数预览 -->
        <el-divider content-position="left">自动计算参数预览</el-divider>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="点数类型">
            {{ form.courseType === '31' ? 'pthpoint' : 'point' }}
          </el-descriptions-item>
          <el-descriptions-item label="课程类型代码">
            {{ form.courseType }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            {{ form.status }}
          </el-descriptions-item>
          <el-descriptions-item label="date_time">
            {{ dateTime }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 提交按钮 -->
        <el-form-item style="margin-top: 30px">
          <el-button type="primary" size="large" :loading="loading" @click="submitForm">
            ✓ 创建预约
          </el-button>
          <el-button size="large" @click="previewJSON">
            预览请求JSON
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { addAppointCn, addAppointEn } from '@/api/appoint'

const loading = ref(false)

const form = ref({
  courseType: '31',
  stuId: '',
  teacherId: '',
  startTime: '',
  usePoint: 'buy',
  courseId: '1406031',
  courseTopId: '1400011',
  courseSubId: '1406021',
  status: 'on',
  remark: ''
})

const endTime = computed(() => {
  if (!form.value.startTime) return ''
  const start = new Date(form.value.startTime)
  const end = new Date(start.getTime() + 30 * 60 * 1000)
  // 修复：使用本地时间格式化，避免 toISOString() 的时区问题
  const year = end.getFullYear()
  const month = String(end.getMonth() + 1).padStart(2, '0')
  const day = String(end.getDate()).padStart(2, '0')
  const hours = String(end.getHours()).padStart(2, '0')
  const minutes = String(end.getMinutes()).padStart(2, '0')
  const seconds = String(end.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
})

const dateTime = computed(() => {
  if (!form.value.startTime) return ''
  const start = new Date(form.value.startTime)
  // 修复：使用本地时间而不是 toISOString()
  const year = start.getFullYear()
  const month = String(start.getMonth() + 1).padStart(2, '0')
  const day = String(start.getDate()).padStart(2, '0')
  const dateStr = `${year}${month}${day}`
  const hour = start.getHours()
  const minute = start.getMinutes()
  const timeNum = hour * 2 + (minute >= 30 ? 2 : 1)
  return `${dateStr}_${timeNum}`
})

const onCourseTypeChange = () => {
  ElMessage.info('请根据课程类型填写对应的教师ID')
}

const previewJSON = () => {
  const requestData = buildRequestData()
  ElMessageBox.alert(
    `<pre>${JSON.stringify(requestData, null, 2)}</pre>`,
    '请求JSON预览',
    { dangerouslyUseHTMLString: true, confirmButtonText: '关闭' }
  )
}

const buildRequestData = () => {
  const pointType = form.value.courseType === '31' ? 'pthpoint' : 'point'
  return {
    stu_id: form.value.stuId,
    t_id: form.value.teacherId,
    start_time: form.value.startTime,
    end_time: endTime.value,
    date_time: dateTime.value,
    course_type: form.value.courseType,
    point_type: pointType,
    use_point: form.value.usePoint,
    status: form.value.status,
    course_id: form.value.courseId,
    course_top_id: form.value.courseTopId,
    course_sub_id: form.value.courseSubId,
    remark: form.value.remark
  }
}

const submitForm = async () => {
  if (!form.value.stuId) {
    ElMessage.error('请填写学生ID')
    return
  }
  if (!form.value.teacherId) {
    ElMessage.error('请填写教师ID')
    return
  }
  if (!form.value.startTime) {
    ElMessage.error('请选择开始时间')
    return
  }

  loading.value = true
  try {
    const requestData = buildRequestData()
    const api = form.value.courseType === '31' ? addAppointCn : addAppointEn
    const result = await api(requestData)

    if (result.code === '10000') {
      ElMessage.success('预约创建成功！')
      resetForm()
    } else {
      ElMessage.error(`创建失败: ${result.message}`)
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value = {
    courseType: '31',
    stuId: '',
    teacherId: '',
    startTime: '',
    usePoint: 'buy',
    courseId: '1001',
    courseTopId: '100',
    courseSubId: '10',
    status: 'on',
    remark: ''
  }
}
</script>

<style scoped>
.add-appoint-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

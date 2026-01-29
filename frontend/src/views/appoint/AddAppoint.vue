<template>
  <div class="add-appoint-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>添加课程预约</span>
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
            <el-radio label="39">阿教</el-radio>
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
            value-format="YYYY-MM-DD HH:mm:ss"
            popper-class="custom-time-picker"
            :disabled-minutes="disabledMinutes"
            :disabled-seconds="disabledSeconds" />
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            💡 时间只能选择整点（00:00）或半点（30:00）
          </div>
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
          <el-radio-group v-model="form.usePoint" @change="onUsePointChange">
            <el-radio label="free">体验课(free)</el-radio>
            <el-radio label="buy">付费课(buy)</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="教材ID" required>
          <el-space direction="vertical" style="width: 100%">
            <el-input v-model="form.levelId" placeholder="自动填充或手动输入">
              <template #prepend>一级教材ID (level_id)</template>
            </el-input>
            <el-input v-model="form.unitId" placeholder="自动填充或手动输入">
              <template #prepend>二级教材ID (unit_id)</template>
            </el-input>
            <el-input v-model="form.courseId" placeholder="自动填充或手动输入">
              <template #prepend>三级教材ID (course_id)</template>
            </el-input>
          </el-space>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            💡 切换课程类型会自动填充默认教材ID,也可手动修改
          </div>
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
            {{ getPointType() }}
          </el-descriptions-item>
          <el-descriptions-item label="课程类型代码">
            {{ form.courseType }}
          </el-descriptions-item>
          <el-descriptions-item label="课程种类(category)">
            {{ getCategory() }}
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

    <!-- 预约结果回显 -->
    <el-card v-if="appointResult" class="result-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>预约成功信息</span>
          <el-tag type="success">已创建</el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="预约ID">
          <el-tag type="primary" size="large">{{ appointResult.appointId }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="课程类型">
          <el-tag :type="appointResult.courseType === '31' ? 'warning' : appointResult.courseType === '39' ? 'danger' : 'success'">
            {{ appointResult.courseType === '31' ? '普通话' : appointResult.courseType === '39' ? '阿教' : '英语' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="学生ID">
          {{ appointResult.stuId }}
        </el-descriptions-item>
        <el-descriptions-item label="教师ID">
          {{ appointResult.teacherId }}
        </el-descriptions-item>
        <el-descriptions-item label="开始时间">
          {{ appointResult.startTime }}
        </el-descriptions-item>
        <el-descriptions-item label="结束时间">
          {{ appointResult.endTime }}
        </el-descriptions-item>
        <el-descriptions-item label="课程性质">
          <el-tag :type="appointResult.usePoint === 'buy' ? 'primary' : 'info'">
            {{ appointResult.usePoint === 'buy' ? '付费课' : '体验课' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="点数类型">
          {{ appointResult.pointType }}
        </el-descriptions-item>
        <el-descriptions-item label="课程种类(category)">
          {{ appointResult.category }}
        </el-descriptions-item>
        <el-descriptions-item label="时间编号">
          {{ appointResult.dateTime }}
        </el-descriptions-item>
        <el-descriptions-item label="预约状态">
          <el-tag :type="appointResult.status === 'on' ? 'success' : 'info'">
            {{ appointResult.status === 'on' ? '正常' : '已取消' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="course_id" :span="2">
          {{ appointResult.courseId }}
        </el-descriptions-item>
        <el-descriptions-item label="level_id">
          {{ appointResult.levelId }}
        </el-descriptions-item>
        <el-descriptions-item label="unit_id">
          {{ appointResult.unitId }}
        </el-descriptions-item>
        <el-descriptions-item v-if="appointResult.remark" label="备注" :span="2">
          {{ appointResult.remark }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">
          <el-tag type="info">{{ appointResult.createTime }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { addAppointCn, addAppointEn } from '@/api/appoint'

const loading = ref(false)

// 预约结果数据
const appointResult = ref(null)

const form = ref({
  courseType: '1',  // 默认英语课程
  stuId: '',
  teacherId: '',
  startTime: '',
  usePoint: 'buy',  // 默认付费课
  levelId: '1161041',  // 一级教材ID (默认英语付费课)
  unitId: '1163731',  // 二级教材ID (默认英语付费课)
  courseId: '1166431',     // 三级教材ID (默认英语付费课)
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

// 根据课程类型和课程性质更新教材ID
const updateCourseIds = () => {
  const courseType = form.value.courseType
  const usePoint = form.value.usePoint

  if (courseType === '1' && usePoint === 'buy') {
    // 英语付费课 (H5 L1-U17-L8)
    form.value.courseId = '1166431'
    form.value.levelId = '1161041'
    form.value.unitId = '1163731'
  } else if (courseType === '1' && usePoint === 'free') {
    // 英语体验课 (新默认值)
    form.value.courseId = '1521751'
    form.value.levelId = '20000'
    form.value.unitId = '607292'
  } else if (courseType === '31' && usePoint === 'buy') {
    // 普通话付费课
    form.value.courseId = '1406031'
    form.value.levelId = '1400011'
    form.value.unitId = '1406021'
  } else if (courseType === '31' && usePoint === 'free') {
    // 普通话体验课 (新默认值)
    form.value.courseId = '1521751'
    form.value.levelId = '20000'
    form.value.unitId = '607292'
  } else if (courseType === '39' && usePoint === 'buy') {
    // 阿教付费课 (使用与英语付费课相同的教材ID)
    form.value.courseId = '1166431'
    form.value.levelId = '1161041'
    form.value.unitId = '1163731'
  } else if (courseType === '39' && usePoint === 'free') {
    // 阿教体验课 (新默认值)
    form.value.courseId = '1521751'
    form.value.levelId = '20000'
    form.value.unitId = '607292'
  }
}

const onCourseTypeChange = () => {
  updateCourseIds()
  const courseType = form.value.courseType
  const usePoint = form.value.usePoint
  let courseTypeName = ''
  let teacherIdHint = ''

  if (courseType === '31') {
    courseTypeName = '普通话'
    teacherIdHint = '350012781'
  } else if (courseType === '1') {
    courseTypeName = '英语'
    teacherIdHint = '2821'
  } else if (courseType === '39') {
    courseTypeName = '阿教'
    teacherIdHint = '360107171'
  }

  const usePointName = usePoint === 'buy' ? '付费课' : '体验课'
  ElMessage.success(`已切换为${courseTypeName}${usePointName}，教师ID参考: ${teacherIdHint}，教材ID已自动填充`)
}

const onUsePointChange = () => {
  updateCourseIds()
  const courseType = form.value.courseType
  const usePoint = form.value.usePoint
  let courseTypeName = ''

  if (courseType === '31') {
    courseTypeName = '普通话'
  } else if (courseType === '1') {
    courseTypeName = '英语'
  } else if (courseType === '39') {
    courseTypeName = '阿教'
  }

  const usePointName = usePoint === 'buy' ? '付费课' : '体验课'
  ElMessage.success(`已切换为${courseTypeName}${usePointName}，教材ID已自动填充`)
}

const previewJSON = () => {
  const requestData = buildRequestData()
  ElMessageBox.alert(
    `<pre>${JSON.stringify(requestData, null, 2)}</pre>`,
    '请求JSON预览',
    { dangerouslyUseHTMLString: true, confirmButtonText: '关闭' }
  )
}

// 计算点数类型
const getPointType = () => {
  const courseType = form.value.courseType
  const usePoint = form.value.usePoint

  if (courseType === '31') {
    return 'pthpoint'  // 普通话
  } else if (courseType === '39' && usePoint === 'buy') {
    return 'ar_point'  // 阿语付费课
  } else {
    return 'point'     // 英语或阿语体验课
  }
}

// 计算课程种类
const getCategory = () => {
  const courseType = form.value.courseType
  const usePoint = form.value.usePoint

  if (courseType === '39') {
    return 'unkown'  // 阿语课程
  } else {
    return `ph_${usePoint}`  // 其他课程
  }
}

const buildRequestData = () => {
  return {
    stu_id: form.value.stuId,
    t_id: form.value.teacherId,
    start_time: form.value.startTime,
    end_time: endTime.value,
    date_time: dateTime.value,
    course_type: form.value.courseType,
    point_type: getPointType(),
    use_point: form.value.usePoint,
    status: form.value.status,
    course_id: form.value.courseId,
    level_id: form.value.levelId,
    unit_id: form.value.unitId,
    category: getCategory(),
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
  // 验证教材ID是否已填写
  if (!form.value.levelId || !form.value.unitId || !form.value.courseId) {
    ElMessage.error('请填写完整的教材ID (一级、二级、三级)')
    return
  }

  loading.value = true
  try {
    const requestData = buildRequestData()
    // 普通话使用addAppointCn，英语和阿教使用addAppointEn
    const api = form.value.courseType === '31' ? addAppointCn : addAppointEn
    const result = await api(requestData)

    if (result.code === '10000') {
      ElMessage.success('预约创建成功！')

      // 保存预约结果用于回显
      appointResult.value = {
        appointId: result.res?.id || '未知',
        courseType: form.value.courseType,
        stuId: form.value.stuId,
        teacherId: form.value.teacherId,
        startTime: form.value.startTime,
        endTime: endTime.value,
        dateTime: dateTime.value,
        usePoint: form.value.usePoint,
        pointType: getPointType(),
        status: form.value.status,
        courseId: form.value.courseId,
        levelId: form.value.levelId,
        unitId: form.value.unitId,
        category: getCategory(),
        remark: form.value.remark,
        createTime: new Date().toLocaleString('zh-CN')
      }

      // 滚动到结果区域
      setTimeout(() => {
        const resultCard = document.querySelector('.result-card')
        if (resultCard) {
          resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }, 100)
    } else {
      // 更详细的错误提示
      let errorMsg = `创建失败: ${result.message || '未知错误'}`

      if (result.code === '11000') {
        errorMsg += '\n\n可能原因：\n' +
          '1. 学生ID或教师ID不存在或状态异常\n' +
          '2. 该时间段已有预约冲突\n' +
          '3. 学生没有该课程的学习权限\n' +
          '4. 教材ID配置错误\n\n' +
          '💡 建议：先使用普通话课程测试（教师ID: 350012781）'
      }

      ElMessageBox.alert(errorMsg, '预约创建失败', {
        confirmButtonText: '知道了',
        type: 'error'
      })
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  // 清空表单
  form.value = {
    courseType: '1',
    stuId: '',
    teacherId: '',
    startTime: '',
    usePoint: 'buy',  // 默认付费课
    courseId: '1166431',      // 英语付费课默认值
    levelId: '1161041',
    unitId: '1163731',
    status: 'on',
    remark: ''
  }

  // 清空预约结果
  appointResult.value = null
}

// 时间选择器：禁用分钟（只允许00和30）
const disabledMinutes = (hour) => {
  // Element Plus 会传入当前选中的小时，返回要禁用的分钟数组
  const disabled = []
  for (let i = 0; i < 60; i++) {
    if (i !== 0 && i !== 30) {
      disabled.push(i)
    }
  }
  return disabled
}

// 时间选择器：禁用秒钟（统一为00秒）
const disabledSeconds = (hour, minute) => {
  // Element Plus 会传入当前选中的小时和分钟，返回要禁用的秒数组
  const disabled = []
  for (let i = 1; i < 60; i++) {
    disabled.push(i)
  }
  return disabled
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

<style>
/* 全局样式：隐藏自定义时间选择器中被禁用的选项 */
.custom-time-picker .el-time-spinner__item.is-disabled {
  display: none !important;
}

/* 备用方案：针对所有时间选择器 */
.el-picker__popper .el-time-spinner__item.is-disabled {
  display: none !important;
}
</style>

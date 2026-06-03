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
          <HistoryInput v-model="form.stuId" placeholder="请输入学生ID" storage-key="add-appoint_stuId" />
        </el-form-item>

        <el-form-item label="教师ID" required>
          <HistoryInput v-model="form.teacherId" placeholder="请填写数字" storage-key="add-appoint_teacherId">
            <template #append>只能填写数字</template>
          </HistoryInput>
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

        <el-form-item label="教材类型">
          <el-select v-model="form.bookType" @change="onBookTypeChange" style="width: 200px;">
            <el-option label="PDF (book_type=0)" value="0" />
            <el-option label="H5 (book_type=1)" value="1" />
            <el-option label="Cocos (book_type=2)" value="2" />
          </el-select>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            💡 选择Cocos时，教材ID(course_id)会自动设置为1883121，并在预约成功后同步更新相关数据库
          </div>
        </el-form-item>

        <el-form-item label="课程性质">
          <el-radio-group v-model="form.usePoint" @change="onUsePointChange">
            <el-radio label="free">体验课(free)</el-radio>
            <el-radio label="buy">付费课(buy)</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="教材选择">
          <el-radio-group v-model="textbookMode" @change="onTextbookModeChange" style="margin-bottom: 10px;">
            <el-radio-button value="cascade">级联选择</el-radio-button>
            <el-radio-button value="input">直接输入ID</el-radio-button>
          </el-radio-group>

          <!-- 模式一：级联下拉 -->
          <template v-if="textbookMode === 'cascade'">
            <el-space direction="vertical" style="width: 100%">
              <el-input-group style="width: 100%">
                <template #prepend><span style="width: 160px; display: inline-block;">一级教材 (level_id)</span></template>
                <el-select
                  v-model="form.levelId"
                  filterable
                  clearable
                  placeholder="请选择一级教材"
                  style="width: 100%"
                  :loading="levelLoading"
                  @change="onLevelChange"
                >
                  <el-option v-for="item in levelOptions" :key="item.id" :label="`[${item.id}] ${item.name}`" :value="String(item.id)" />
                </el-select>
                <template #append>
                  <el-button :loading="levelLoading" @click="loadLevelOptions">刷新</el-button>
                </template>
              </el-input-group>

              <el-input-group style="width: 100%">
                <template #prepend><span style="width: 160px; display: inline-block;">二级教材 (unit_id)</span></template>
                <el-select
                  v-model="form.unitId"
                  filterable
                  clearable
                  placeholder="请先选择一级教材"
                  style="width: 100%"
                  :loading="unitLoading"
                  :disabled="!form.levelId"
                  @change="onUnitChange"
                >
                  <el-option v-for="item in unitOptions" :key="item.id" :label="`[${item.id}] ${item.name}`" :value="String(item.id)" />
                </el-select>
              </el-input-group>

              <el-input-group style="width: 100%">
                <template #prepend><span style="width: 160px; display: inline-block;">三级教材 (course_id)</span></template>
                <el-select
                  v-model="form.courseId"
                  filterable
                  clearable
                  placeholder="请先选择二级教材"
                  style="width: 100%"
                  :loading="courseLoading"
                  :disabled="!form.unitId"
                >
                  <el-option v-for="item in courseOptions" :key="item.id" :label="`[${item.id}] ${item.name}`" :value="String(item.id)" />
                </el-select>
              </el-input-group>
            </el-space>
            <div style="color: #909399; font-size: 12px; margin-top: 5px;">
              💡 选择一级后自动加载二级，选择二级后自动加载三级
            </div>
          </template>

          <!-- 模式二：直接输入ID反查 -->
          <template v-else>
            <el-space direction="vertical" style="width: 100%">
              <el-input-group style="width: 100%">
                <template #prepend><span style="width: 160px; display: inline-block;">一级教材ID (level_id)</span></template>
                <el-input v-model="form.levelId" placeholder="自动填充或手动输入" />
              </el-input-group>

              <el-input-group style="width: 100%">
                <template #prepend><span style="width: 160px; display: inline-block;">二级教材ID (unit_id)</span></template>
                <el-input
                  v-model="form.unitId"
                  placeholder="输入后自动查询一级"
                  :loading="ancestorLoading"
                  @blur="onUnitIdBlur"
                />
                <template #append>
                  <el-button :loading="ancestorLoading" @click="onUnitIdBlur">查询</el-button>
                </template>
              </el-input-group>

              <el-input-group style="width: 100%">
                <template #prepend><span style="width: 160px; display: inline-block;">三级教材ID (course_id)</span></template>
                <el-input
                  v-model="form.courseId"
                  placeholder="输入后自动回填一级和二级"
                  :loading="ancestorLoading"
                  @blur="onCourseIdBlur"
                />
                <template #append>
                  <el-button :loading="ancestorLoading" @click="onCourseIdBlur">查询</el-button>
                </template>
              </el-input-group>
            </el-space>
            <div style="color: #909399; font-size: 12px; margin-top: 5px;">
              💡 输入二级或三级ID后点击查询/失焦，自动反查并填充上级ID
            </div>
          </template>
        </el-form-item>

        <!-- 其他设置 -->
        <el-divider content-position="left">其他设置</el-divider>

        <el-form-item label="财富类型">
          <HistoryInput v-model="form.pointType" placeholder="自动计算或手动输入" storage-key="add-appoint_pointType">
            <template #append>
              <el-button @click="form.pointType = getPointType()">重置为自动值</el-button>
            </template>
          </HistoryInput>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            💡 默认根据课程类型自动计算，也可手动修改
          </div>
        </el-form-item>

        <el-form-item label="消耗数量">
          <el-input-number v-model="form.costNum" :min="0" :max="999" style="width: 100%;" />
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            💡 设置本次预约消耗的财富数量
          </div>
        </el-form-item>

        <el-form-item label="上课方式">
          <el-select v-model="form.teachType" style="width: 200px;">
            <el-option label="AC上课 (51TalkAC)" value="51TalkAC" />
            <el-option label="网页版上课 (WebAc)" value="WebAc" />
          </el-select>
        </el-form-item>

        <el-form-item v-if="form.teachType === 'WebAc'" label="界面语言">
          <el-select v-model="form.langcode" style="width: 220px;">
            <el-option label="英语 (en)" value="en" />
            <el-option label="简体中文 (zh-CN)" value="zh-CN" />
            <el-option label="繁体中文-香港 (zh-HK)" value="zh-HK" />
            <el-option label="繁体中文-台湾 (zh-TW)" value="zh-TW" />
            <el-option label="马来语 (ms)" value="ms" />
            <el-option label="泰语 (th)" value="th" />
            <el-option label="阿拉伯语-沙特 (ar-SA)" value="ar-SA" />
            <el-option label="日语 (ja)" value="ja" />
            <el-option label="土耳其语 (tr)" value="tr" />
            <el-option label="西班牙语 (es)" value="es" />
            <el-option label="越南语 (vi)" value="vi" />
            <el-option label="印尼语 (id)" value="id" />
            <el-option label="韩语 (ko)" value="ko" />
            <el-option label="葡萄牙语-巴西 (pt-BR)" value="pt-BR" />
            <el-option label="芬兰语 (fi)" value="fi" />
            <el-option label="波兰语 (pl)" value="pl" />
          </el-select>
        </el-form-item>

        <el-form-item label="预约状态">
          <el-select v-model="form.status">
            <el-option label="正常(on)" value="on" />
            <el-option label="取消(cancel)" value="cancel" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注信息">
          <HistoryInput v-model="form.remark" type="textarea" :rows="2" placeholder="选填" storage-key="add-appoint_remark" />
        </el-form-item>

        <!-- 参数预览 -->
        <el-divider content-position="left">自动计算参数预览</el-divider>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="点数类型">
            {{ form.pointType || getPointType() }}
          </el-descriptions-item>
          <el-descriptions-item label="消耗数量">
            {{ form.costNum }}
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
          <el-button
            v-if="appointResult && form.teachType === 'WebAc'"
            type="success"
            size="large"
            :loading="classLinkLoading"
            @click="generateClassLink">
            生成学员上课链接
          </el-button>
          <el-button
            v-if="appointResult && form.teachType === 'WebAc'"
            type="warning"
            size="large"
            :loading="teacherLinkLoading"
            @click="generateTeacherLink">
            生成老师上课链接
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
        <el-descriptions-item label="教材类型">
          <el-tag :type="appointResult.bookType === '2' ? 'danger' : appointResult.bookType === '1' ? 'success' : 'warning'">
            {{ appointResult.bookType === '0' ? 'PDF' : appointResult.bookType === '1' ? 'H5' : 'Cocos' }}
          </el-tag>
          <el-button
            v-if="appointResult.bookType === '1' || appointResult.bookType === '2'"
            type="warning"
            size="small"
            :loading="cocosLoading"
            style="margin-left: 8px;"
            @click="syncCocos">
            同步教材数据库
          </el-button>
        </el-descriptions-item>
        <el-descriptions-item label="点数类型">
          {{ appointResult.pointType }}
        </el-descriptions-item>
        <el-descriptions-item label="消耗数量">
          <el-tag type="warning">{{ appointResult.costNum }}</el-tag>
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
import { addAppointCn, addAppointEn, syncCocosBookType, getClassToken } from '@/api/appoint'
import axios from 'axios'

const loading = ref(false)
const cocosLoading = ref(false)
const classLinkLoading = ref(false)
const teacherLinkLoading = ref(false)

// 预约结果数据
const appointResult = ref(null)

// ===== 教材选择相关 =====
const textbookMode = ref('input') // 'cascade' | 'input'

// 级联下拉数据
const levelOptions = ref([])
const unitOptions = ref([])
const courseOptions = ref([])
const levelLoading = ref(false)
const unitLoading = ref(false)
const courseLoading = ref(false)

// 反查加载状态
const ancestorLoading = ref(false)

// 查询子节点，返回 children 数组
const fetchSubtree = async (id) => {
  const res = await axios.get(`/textbook/series_textbook/query_subtree_by_id`, { params: { id } })
  if (res.data?.code === '10000') {
    return res.data.res?.children || []
  }
  return []
}

// 查询祖先，返回 { node, parent } 结构
const fetchAncestor = async (id) => {
  const res = await axios.get(`/textbook/series_textbook/query_ancestor_by_id`, { params: { id } })
  if (res.data?.code === '10000') {
    return res.data.res || null
  }
  return null
}

// 从 tree_path 解析各层级id，格式 "0,level,unit,course"
const parseTreePath = (treePath) => {
  if (!treePath) return {}
  const parts = treePath.split(',').filter(p => p !== '0')
  return {
    levelId: parts[0] || '',
    unitId: parts[1] || '',
    courseId: parts[2] || ''
  }
}

// 加载一级教材：用当前 levelId 查子树得到兄弟节点（即先查父节点的子树）
// 策略：直接查 levelId 对应节点的子树作为二级；一级列表通过 ancestor 接口的 parent 获取同级
const loadLevelOptions = async () => {
  levelLoading.value = true
  try {
    // 先通过 ancestor 接口获取当前 levelId 的父节点，再用父节点查子树得到所有一级兄弟
    const currentLevelId = form.value.levelId || '1161041'
    const ancestorData = await fetchAncestor(currentLevelId)
    const parentId = ancestorData?.parent?.id
    if (parentId) {
      levelOptions.value = await fetchSubtree(parentId)
    } else {
      // 当前节点已是顶级，直接作为一个选项
      if (ancestorData) {
        levelOptions.value = [{ id: ancestorData.id, name: ancestorData.name }]
      }
    }
  } catch (e) {
    ElMessage.error('加载一级教材失败')
  } finally {
    levelLoading.value = false
  }
}

// 选择一级后加载二级
const onLevelChange = async (val) => {
  form.value.unitId = ''
  form.value.courseId = ''
  unitOptions.value = []
  courseOptions.value = []
  if (!val) return
  unitLoading.value = true
  try {
    unitOptions.value = await fetchSubtree(val)
  } catch (e) {
    ElMessage.error('加载二级教材失败')
  } finally {
    unitLoading.value = false
  }
}

// 选择二级后加载三级
const onUnitChange = async (val) => {
  form.value.courseId = ''
  courseOptions.value = []
  if (!val) return
  courseLoading.value = true
  try {
    courseOptions.value = await fetchSubtree(val)
  } catch (e) {
    ElMessage.error('加载三级教材失败')
  } finally {
    courseLoading.value = false
  }
}

// 输入二级ID后反查一级（tree_depth=2，parent 是一级）
const onUnitIdBlur = async () => {
  const id = form.value.unitId
  if (!id) return
  ancestorLoading.value = true
  try {
    const data = await fetchAncestor(id)
    if (data) {
      // 用 tree_path 解析
      const parsed = parseTreePath(data.tree_path)
      if (parsed.levelId) {
        form.value.levelId = parsed.levelId
        ElMessage.success(`已自动填充一级教材ID: ${parsed.levelId}`)
      } else if (data.parent?.id) {
        form.value.levelId = String(data.parent.id)
        ElMessage.success(`已自动填充一级教材ID: ${data.parent.id}`)
      }
    }
  } catch (e) {
    ElMessage.error('查询祖先节点失败')
  } finally {
    ancestorLoading.value = false
  }
}

// 输入三级ID后反查一级和二级（tree_path: "0,level,unit,course"）
const onCourseIdBlur = async () => {
  const id = form.value.courseId
  if (!id) return
  ancestorLoading.value = true
  try {
    const data = await fetchAncestor(id)
    if (data) {
      const parsed = parseTreePath(data.tree_path)
      if (parsed.levelId) form.value.levelId = parsed.levelId
      if (parsed.unitId) form.value.unitId = parsed.unitId
      if (parsed.levelId || parsed.unitId) {
        ElMessage.success(`已自动填充：一级=${parsed.levelId}，二级=${parsed.unitId}`)
      }
    }
  } catch (e) {
    ElMessage.error('查询祖先节点失败')
  } finally {
    ancestorLoading.value = false
  }
}

// 切换教材选择模式
const onTextbookModeChange = (mode) => {
  if (mode === 'cascade') {
    syncCascadeFromCurrent()
  }
}

// 根据当前三个 ID 同步级联下拉数据（无论哪种模式都调用）
// 直接输入模式：用 tree_path 回填已有，无需额外操作（ID已在form里）
// 级联模式：需要加载各级下拉选项并选中当前值
const syncCascadeFromCurrent = async () => {
  if (textbookMode.value !== 'cascade') return
  // 加载一级列表
  await loadLevelOptions()
  // 加载二级列表（基于当前 levelId）
  if (form.value.levelId) {
    unitLoading.value = true
    try {
      unitOptions.value = await fetchSubtree(form.value.levelId)
    } catch (e) { /* ignore */ } finally {
      unitLoading.value = false
    }
  }
  // 加载三级列表（基于当前 unitId）
  if (form.value.unitId) {
    courseLoading.value = true
    try {
      courseOptions.value = await fetchSubtree(form.value.unitId)
    } catch (e) { /* ignore */ } finally {
      courseLoading.value = false
    }
  }
}

const form = ref({
  courseType: '1',  // 默认英语课程
  stuId: '',
  teacherId: '',
  startTime: '',
  usePoint: 'buy',  // 默认付费课
  bookType: '0',   // 教材类型（付费课默认PDF）
  levelId: '1161041',  // 一级教材ID (默认英语付费课)
  unitId: '1163731',  // 二级教材ID (默认英语付费课)
  courseId: '1166431',     // 三级教材ID (默认英语付费课)
  pointType: '',  // 财富类型（空则自动计算）
  costNum: 1,  // 消耗数量（默认1）
  teachType: '51TalkAC',  // 上课方式（默认AC上课）
  langcode: 'en',         // 界面语言（默认英语）
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

// 根据课程类型和课程性质更新教材ID，并同步级联/反查
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
  // 三个 ID 已确定，同步级联下拉（级联模式才执行）
  syncCascadeFromCurrent()
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
  // 切换到付费课时，重置教材类型为PDF(不需要同步)并恢复教材ID
  if (form.value.usePoint === 'buy') {
    form.value.bookType = '0'
  }
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

const onBookTypeChange = () => {
  if (form.value.bookType === '2') {
    // Cocos教材：固定三级ID，同时设置对应的一二级
    form.value.courseId = '1883121'
    form.value.unitId = '1799471'
    form.value.levelId = '20000'
    // 同步级联下拉
    syncCascadeFromCurrent()
    ElMessage.success('已选择Cocos教材，教材ID已自动设置')
  } else {
    // 切换回非Cocos教材：恢复当前课程类型+性质对应的默认教材ID（内部已调用 syncCascadeFromCurrent）
    updateCourseIds()
    const label = form.value.bookType === '0' ? 'PDF' : 'H5'
    ElMessage.success(`已切换为${label}教材，教材ID已恢复默认值`)
  }
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
    point_type: form.value.pointType || getPointType(),  // 优先使用手动输入的值
    cost_num: form.value.costNum,  // 添加消耗数量
    use_point: form.value.usePoint,
    book_type: form.value.bookType,  // 教材类型
    teach_type: form.value.teachType,  // 上课方式
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
        bookType: form.value.bookType,
        pointType: form.value.pointType || getPointType(),
        costNum: form.value.costNum,
        status: form.value.status,
        courseId: form.value.courseId,
        levelId: form.value.levelId,
        unitId: form.value.unitId,
        category: getCategory(),
        remark: form.value.remark,
        createTime: new Date().toLocaleString('zh-CN'),
        cocosSync: result.cocos_sync  // Cocos同步结果
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

const syncCocos = async () => {
  if (!appointResult.value?.appointId) {
    ElMessage.error('未找到预约ID')
    return
  }
  cocosLoading.value = true
  try {
    const result = await syncCocosBookType({ appoint_id: appointResult.value.appointId, book_type: appointResult.value.bookType })
    if (result.code === '10000') {
      ElMessage.success('Cocos数据库同步成功')
    } else {
      ElMessage.error(`同步失败: ${result.message || '未知错误'}`)
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    cocosLoading.value = false
  }
}

const copyToClipboard = async (text) => {
  // 优先使用 Clipboard API（需要 HTTPS 或 localhost）
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text)
    return
  }
  // 移动端兼容方案：用 setSelectionRange 替代 select()
  const el = document.createElement('textarea')
  el.value = text
  el.setAttribute('readonly', '')
  el.style.cssText = 'position:fixed;top:0;left:0;opacity:0;'
  document.body.appendChild(el)
  el.focus()
  el.setSelectionRange(0, el.value.length)
  const ok = document.execCommand('copy')
  document.body.removeChild(el)
  if (!ok) throw new Error('execCommand failed')
}

const generateClassLink = async () => {
  if (!appointResult.value?.appointId || !appointResult.value?.stuId) {
    ElMessage.error('缺少预约ID或学员ID')
    return
  }
  classLinkLoading.value = true
  try {
    const result = await getClassToken(appointResult.value.stuId)
    if (result.code === '10000') {
      const token = result.data.token
      const link = `https://cloud_classroom.middletest.51suyang.cn/?appointId=${appointResult.value.appointId}&relId=${appointResult.value.stuId}&role=stu&javaCourseType=1&token=${token}&buildver=web-1.0.0&langcode=${form.value.langcode}&mock=1&console=1&mockData=1`
      let copied = true
      try { await copyToClipboard(link) } catch { copied = false }
      ElMessageBox.alert(
        `<div style="word-break:break-all;user-select:all;">${link}</div>`,
        copied ? '学员上课链接（已复制到剪贴板）' : '学员上课链接（复制失败，请长按链接手动复制）',
        { dangerouslyUseHTMLString: true, confirmButtonText: '关闭' }
      )
    } else {
      ElMessage.error(`获取 token 失败: ${result.message || '未知错误'}`)
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    classLinkLoading.value = false
  }
}

const generateTeacherLink = async () => {
  if (!appointResult.value?.appointId || !appointResult.value?.teacherId) {
    ElMessage.error('缺少预约ID或教师ID')
    return
  }
  teacherLinkLoading.value = true
  try {
    const result = await getClassToken(appointResult.value.teacherId, 'tea_h5j')
    if (result.code === '10000') {
      const token = result.data.token
      const link = `https://cloud_classroom.middletest.51suyang.cn/?appointId=${appointResult.value.appointId}&relId=${appointResult.value.teacherId}&role=tea&javaCourseType=1&token=${token}&buildver=web-1.0.0&langcode=${form.value.langcode}&mock=1&console=1&mockData=1`
      let copied = true
      try { await copyToClipboard(link) } catch { copied = false }
      ElMessageBox.alert(
        `<div style="word-break:break-all;user-select:all;">${link}</div>`,
        copied ? '老师上课链接（已复制到剪贴板）' : '老师上课链接（复制失败，请长按链接手动复制）',
        { dangerouslyUseHTMLString: true, confirmButtonText: '关闭' }
      )
    } else {
      ElMessage.error(`获取 token 失败: ${result.message || '未知错误'}`)
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    teacherLinkLoading.value = false
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
    bookType: '0',   // 付费课默认PDF
    courseId: '1166431',      // 英语付费课默认值
    levelId: '1161041',
    unitId: '1163731',
    pointType: '',  // 重置为空，自动计算
    costNum: 1,  // 重置为默认值1
    teachType: '51TalkAC',  // 上课方式（默认AC上课）
    langcode: 'en',         // 界面语言（默认英语）
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

<template>
  <div class="appoint-list-page">
    <el-card>
      <template #header>
        <span><strong>测试环境</strong>预约列表管理</span>
      </template>

      <!-- 查询工具栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="预约ID">
            <el-input v-model="searchForm.appointId" placeholder="请输入预约ID" clearable style="width: 160px" />
          </el-form-item>
          <el-form-item label="学生ID">
            <el-input v-model="searchForm.stuId" placeholder="请输入学生ID" clearable style="width: 160px" />
          </el-form-item>
          <el-form-item label="教师ID">
            <el-input v-model="searchForm.tId" placeholder="请输入教师ID" clearable style="width: 160px" />
          </el-form-item>
          <el-form-item label="教材ID">
            <el-input v-model="searchForm.courseId" placeholder="请输入教材ID" clearable style="width: 160px" />
          </el-form-item>
          <el-form-item label="课程类型">
            <el-select v-model="searchForm.courseType" placeholder="请选择" clearable style="width: 180px">
              <el-option label="英语成人（参考）" value="1" />
              <el-option label="英语青少（参考）" value="2" />
              <el-option label="写作课" value="3" />
              <el-option label="南非体验课" value="4" />
              <el-option label="日教陪练课" value="5" />
              <el-option label="阿语陪练课" value="6" />
              <el-option label="AI外教课" value="7" />
              <el-option label="普通话" value="31" />
              <el-option label="背单词正课" value="32" />
              <el-option label="阿语外教" value="39" />
            </el-select>
          </el-form-item>
          <el-form-item label="课程种类">
            <el-select v-model="searchForm.category" placeholder="请选择" clearable style="width: 150px">
              <el-option label="菲教体验课" value="ph_free" />
              <el-option label="菲教付费课" value="ph_buy" />
              <el-option label="欧美付费课" value="ea_buy" />
              <el-option label="美小体验课" value="nat_free" />
              <el-option label="美小付费课" value="nat_buy" />
              <el-option label="阿语课" value="unkown" />

            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 130px">
              <el-option label="正常" value="on" />
              <el-option label="已结束" value="end" />
              <el-option label="学生缺席" value="s_absent" />
              <el-option label="教师缺席" value="t_absent" />
              <el-option label="取消" value="cancel" />
            </el-select>
          </el-form-item>
          <el-form-item label="开始日期">
            <el-date-picker
              v-model="searchForm.startDate"
              type="date"
              placeholder="开始日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              style="width: 150px" />
          </el-form-item>
          <el-form-item label="结束日期">
            <el-date-picker
              v-model="searchForm.endDate"
              type="date"
              placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              style="width: 150px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="Search" @click="handleSearch">查询</el-button>
            <el-button icon="Refresh" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        style="width: 100%">
        <el-table-column prop="id" label="预约ID" width="100" />
        <el-table-column prop="s_id" label="学生ID" width="120" />
        <el-table-column prop="t_id" label="教师ID" width="100" />
        <el-table-column label="课程类型" width="150">
          <template #default="{ row }">
            <el-tag :type="getCourseTypeColor(row.course_type)">
              {{ getCourseTypeText(row.course_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="160" />
        <el-table-column prop="end_time" label="结束时间" width="160" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'on'" type="success">正常</el-tag>
            <el-tag v-else-if="row.status === 'end'" type="info">已结束</el-tag>
            <el-tag v-else-if="row.status === 's_absent'" type="warning">学生缺席</el-tag>
            <el-tag v-else-if="row.status === 't_absent'" type="warning">教师缺席</el-tag>
            <el-tag v-else-if="row.status === 'cancel'" type="danger">取消</el-tag>
            <el-tag v-else type="info">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="课程种类" width="130">
          <template #default="{ row }">
            <el-tag :type="getCategoryColor(row.category)">
              {{ getCategoryText(row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_time" label="时间编号" width="140" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleViewDetail(row)">详情</el-button>
            <el-dropdown @command="(status) => handleStatusChange(row, status)" trigger="click">
              <el-button type="warning" link>
                变更状态 <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="on" :disabled="row.status === 'on'">
                    <el-tag type="success" size="small">正常</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item command="end" :disabled="row.status === 'end'">
                    <el-tag type="info" size="small">已结束</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item command="s_absent" :disabled="row.status === 's_absent'">
                    <el-tag type="warning" size="small">学生缺席</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item command="t_absent" :disabled="row.status === 't_absent'">
                    <el-tag type="warning" size="small">教师缺席</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item command="cancel" :disabled="row.status === 'cancel'">
                    <el-tag type="danger" size="small">取消</el-tag>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="预约详情" width="600px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="预约ID">{{ currentRow.id }}</el-descriptions-item>
        <el-descriptions-item label="学生ID">{{ currentRow.s_id }}</el-descriptions-item>
        <el-descriptions-item label="教师ID">{{ currentRow.t_id }}</el-descriptions-item>
        <el-descriptions-item label="课程类型">
          <el-tag :type="getCourseTypeColor(currentRow.course_type)">
            {{ getCourseTypeText(currentRow.course_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="开始时间" :span="2">{{ currentRow.start_time }}</el-descriptions-item>
        <el-descriptions-item label="结束时间" :span="2">{{ currentRow.end_time }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag v-if="currentRow.status === 'on'" type="success">正常</el-tag>
          <el-tag v-else-if="currentRow.status === 'end'" type="info">已结束</el-tag>
          <el-tag v-else-if="currentRow.status === 's_absent'" type="warning">学生缺席</el-tag>
          <el-tag v-else-if="currentRow.status === 't_absent'" type="warning">教师缺席</el-tag>
          <el-tag v-else-if="currentRow.status === 'cancel'" type="danger">取消</el-tag>
          <el-tag v-else type="info">{{ currentRow.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="点数类型">{{ currentRow.point_type }}</el-descriptions-item>
        <el-descriptions-item label="课程种类" :span="2">
          <el-tag :type="getCategoryColor(currentRow.category)">
            {{ getCategoryText(currentRow.category) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="课程ID">{{ currentRow.course_id }}</el-descriptions-item>
        <el-descriptions-item label="一级教材ID (level_id)">{{ currentRow.level_id }}</el-descriptions-item>
        <el-descriptions-item label="二级教材ID (unit_id)">{{ currentRow.unit_id }}</el-descriptions-item>
        <el-descriptions-item label="时间编号" :span="2">{{ currentRow.date_time }}</el-descriptions-item>
        <el-descriptions-item label="添加时间" :span="2">{{ currentRow.add_time }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { getAppointList, updateAppointStatus } from '@/api/appoint'

const loading = ref(false)
const tableData = ref([])
const detailVisible = ref(false)
const currentRow = ref(null)

const searchForm = ref({
  appointId: '',
  stuId: '',
  tId: '',
  courseId: '',
  courseType: '',
  category: '',
  status: '',
  startDate: '',
  endDate: ''
})

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

// 状态文本映射
const statusTextMap = {
  'on': '正常',
  'end': '已结束',
  's_absent': '学生缺席',
  't_absent': '教师缺席',
  'cancel': '取消'
}

// 课程类型映射
const courseTypeMap = {
  '1': '英语成人（参考）',
  '2': '英语青少（参考）',
  '3': '写作课',
  '4': '南非体验课',
  '5': '日教陪练课',
  '6': '阿语陪练课',
  '7': 'AI外教课',
  '31': '普通话',
  '32': '背单词正课',
  '39': '阿语外教课'
}

// 课程种类映射
const categoryMap = {
  'ph_free': '菲教体验课',
  'ph_buy': '菲教付费课',
  'ea_buy': '欧美付费课',
  'nat_free': '美小体验课',
  'unkown': '阿语课',
  'nat_buy': '美小付费课'
}

// 获取课程类型文本
const getCourseTypeText = (courseType) => {
  return courseTypeMap[String(courseType)] || `未知(${courseType})`
}

// 获取课程类型标签颜色
const getCourseTypeColor = (courseType) => {
  const type = String(courseType)
  if (type === '31') return 'success'      // 普通话 - 绿色
  if (type === '1') return 'primary'       // 英语成人 - 蓝色
  if (type === '2') return ''              // 英语青少 - 默认色
  if (type === '7') return 'warning'       // AI外教 - 橙色
  return 'info'                            // 其他 - 灰色
}

// 获取课程种类文本
const getCategoryText = (category) => {
  return categoryMap[category] || category || '未知'
}

// 获取课程种类标签颜色
const getCategoryColor = (category) => {
  if (category === 'ph_buy' || category === 'ea_buy' || category === 'nat_buy') {
    return 'warning'  // 付费课 - 橙色
  }
  if (category === 'ph_free' || category === 'nat_free') {
    return 'success'  // 体验课 - 绿色
  }
  return 'info'       // 其他 - 灰色
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      pageSize: pagination.value.pageSize,
      appointId: searchForm.value.appointId,
      stuId: searchForm.value.stuId,
      tId: searchForm.value.tId,
      courseId: searchForm.value.courseId,
      courseType: searchForm.value.courseType,
      category: searchForm.value.category,
      status: searchForm.value.status,
      startDate: searchForm.value.startDate,
      endDate: searchForm.value.endDate
    }

    const result = await getAppointList(params)

    if (result.code === '10000') {
      tableData.value = result.data.list
      pagination.value.total = result.data.total
      ElMessage.success(`查询成功，共 ${result.data.total} 条记录`)
    } else {
      ElMessage.error(`查询失败: ${result.message}`)
    }
  } catch (error) {
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  loadData()
}

const handleReset = () => {
  searchForm.value = {
    appointId: '',
    stuId: '',
    tId: '',
    courseId: '',
    courseType: '',
    category: '',
    status: '',
    startDate: '',
    endDate: ''
  }
  pagination.value.page = 1
  // 重置后不自动查询，需要用户主动点击查询按钮
}

const handlePageChange = (page) => {
  pagination.value.page = page
  loadData()
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.page = 1
  loadData()
}

const handleViewDetail = (row) => {
  currentRow.value = row
  detailVisible.value = true
}

const handleStatusChange = async (row, newStatus) => {
  const oldStatusText = statusTextMap[row.status] || row.status
  const newStatusText = statusTextMap[newStatus] || newStatus

  try {
    await ElMessageBox.confirm(
      `确定将预约 ${row.id} 的状态从「${oldStatusText}」变更为「${newStatusText}」吗？`,
      '状态变更确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 调用API更新状态
    const result = await updateAppointStatus({
      id: row.id,
      status: newStatus
    })

    if (result.code === '10000') {
      ElMessage.success('状态变更成功')
      // 刷新列表
      loadData()
    } else {
      ElMessage.error(`状态变更失败: ${result.message}`)
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(`状态变更失败: ${error.message || error}`)
    }
  }
}

onMounted(() => {
  // 列表默认为空，不自动加载数据
  // 用户需要点击"查询"按钮来加载数据
})
</script>

<style scoped>
.appoint-list-page {
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

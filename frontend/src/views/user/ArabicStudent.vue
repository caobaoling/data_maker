<template>
  <div class="arabic-student">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>阿语学员标签管理</span>
          <el-tag type="warning">仅限测试环境操作</el-tag>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            style="width: 400px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="标签类型" prop="tag_type">
          <el-select
            v-model="form.tag_type"
            placeholder="请选择标签类型"
            style="width: 400px">
            <el-option
              v-for="item in tagTypes"
              :key="item.type"
              :label="`${item.name} (${item.type})`"
              :value="item.type">
              <span style="float: left">{{ item.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.type }}</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleAdd">
            添加标签
          </el-button>
          <el-button type="info" :loading="querying" @click="handleQuery">
            查询标签
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 查询结果 -->
    <el-card v-if="queryResult !== null" class="result-card">
      <template #header>
        <div class="card-header">
          <span>查询结果</span>
          <el-tag type="success">用户 {{ queryResult.user_id }}</el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">{{ queryResult.user_id }}</el-descriptions-item>
        <el-descriptions-item label="标签类型">
          <el-tag type="primary">{{ queryResult.type_name }} ({{ queryResult.type }})</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="接口返回" :span="2">
          <pre class="result-pre">{{ JSON.stringify(queryResult.result, null, 2) }}</pre>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { getArabicTagTypes, queryArabicTag, addArabicTag } from '@/api/user'

const formRef = ref(null)
const tagTypes = ref([])
const submitting = ref(false)
const querying = ref(false)
const queryResult = ref(null)

const form = reactive({
  user_id: '',
  tag_type: ''
})

const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  tag_type: [
    { required: true, message: '请选择标签类型', trigger: 'change' }
  ]
}

const loadTagTypes = async () => {
  try {
    const res = await getArabicTagTypes()
    if (res.code === '0') {
      tagTypes.value = res.data
    } else {
      ElMessage.error(res.msg || '加载标签类型失败')
    }
  } catch (error) {
    ElMessage.error('加载标签类型失败')
  }
}

const handleAdd = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitting.value = true
    const res = await addArabicTag({
      user_id: form.user_id,
      type: form.tag_type
    })
    if (res.code === '0') {
      ElMessage.success('添加标签成功')
      queryResult.value = res.data
    } else {
      ElMessage.error(res.msg || '添加失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('操作失败')
    }
  } finally {
    submitting.value = false
  }
}

const handleQuery = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    querying.value = true
    const res = await queryArabicTag({
      user_id: form.user_id,
      type: form.tag_type
    })
    if (res.code === '0') {
      ElMessage.success('查询成功')
      queryResult.value = res.data
    } else {
      ElMessage.error(res.msg || '查询失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('查询失败')
    }
  } finally {
    querying.value = false
  }
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  queryResult.value = null
}

onMounted(() => {
  loadTagTypes()
})
</script>

<style scoped>
.arabic-student {
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

.result-pre {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-size: 13px;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}
</style>

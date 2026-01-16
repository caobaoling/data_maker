<template>
  <div class="change-level">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>测试环境</strong>修改精灵等级</span>
          <el-tag type="success">调整用户精灵等级和经验值</el-tag>
        </div>
      </template>

      <!-- 修改表单 -->
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input
            v-model="form.user_id"
            placeholder="请输入用户ID"
            clearable
            style="width: 500px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="info" :loading="querying" @click="handleQuery">
            查询当前等级
          </el-button>
        </el-form-item>

        <el-form-item label="目标等级" prop="level">
          <el-select
            v-model="form.level"
            placeholder="请选择目标等级"
            style="width: 500px">
            <el-option
              v-for="item in levelOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
              <span style="float: left">{{ item.label }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{ item.style }}</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            修改等级
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 说明信息 -->
      <el-alert type="info" :closable="false" style="margin-top: 20px">
        <template #title>
          <strong>功能说明</strong>
        </template>
        <ul style="margin: 10px 0; padding-left: 20px">
          <li>修改用户精灵的等级、总经验值、当前经验值和外观代码</li>
          <li>等级范围: 1-10级</li>
          <li>修改后会立即更新数据库中的精灵信息</li>
        </ul>
      </el-alert>
    </el-card>

    <!-- 当前等级信息 -->
    <el-card v-if="currentLevel" class="current-level-card">
      <template #header>
        <div class="card-header">
          <span>当前等级信息</span>
          <el-tag type="info">用户 {{ currentLevel.user_id }}</el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="当前等级">
          <el-tag type="primary" size="large">等级 {{ currentLevel.elf_level }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="外观代码">
          <el-tag type="info">{{ currentLevel.elf_style_code }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="总经验值">
          {{ currentLevel.elf_total_exp }}
        </el-descriptions-item>
        <el-descriptions-item label="当前经验值">
          {{ currentLevel.elf_level_exp }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 修改结果 -->
    <el-card v-if="resultData" class="result-card">
      <template #header>
        <div class="card-header">
          <span>修改结果</span>
          <el-tag type="success">修改成功</el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">
          {{ resultData.user_id }}
        </el-descriptions-item>
        <el-descriptions-item label="目标等级">
          <el-tag type="success">等级 {{ resultData.level }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="总经验值">
          {{ resultData.level_data.elf_total_exp }}
        </el-descriptions-item>
        <el-descriptions-item label="当前经验值">
          {{ resultData.level_data.elf_level_exp }}
        </el-descriptions-item>
        <el-descriptions-item label="外观代码" :span="2">
          <el-tag type="info">{{ resultData.level_data.elf_style_code }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { queryLevel, changeLevel } from '@/api/elf'

// 表单引用
const formRef = ref(null)

// 表单数据
const form = reactive({
  user_id: '',
  level: 1
})

// 等级选项
const levelOptions = [
  { value: 1, label: '等级 1', style: 'elf_egg_001' },
  { value: 2, label: '等级 2', style: 'elf_baby_001' },
  { value: 3, label: '等级 3', style: 'elf_baby_002' },
  { value: 4, label: '等级 4', style: 'elf_baby_003' },
  { value: 5, label: '等级 5', style: 'elf_baby_004' },
  { value: 6, label: '等级 6', style: 'elf_child_002' },
  { value: 7, label: '等级 7', style: 'elf_child_003' },
  { value: 8, label: '等级 8', style: 'elf_young_001' },
  { value: 9, label: '等级 9', style: 'elf_young_001' },
  { value: 10, label: '等级 10', style: 'elf_young_001' }
]

// 表单验证规则
const rules = {
  user_id: [
    { required: true, message: '请输入用户ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '用户ID必须是数字', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择目标等级', trigger: 'change' }
  ]
}

// 查询状态
const querying = ref(false)

// 提交状态
const submitting = ref(false)

// 当前等级信息
const currentLevel = ref(null)

// 修改结果
const resultData = ref(null)

// 查询当前等级
const handleQuery = async () => {
  if (!form.user_id) {
    ElMessage.warning('请先输入用户ID')
    return
  }

  try {
    querying.value = true

    const res = await queryLevel({
      user_id: form.user_id
    })

    if (res.code === '0') {
      currentLevel.value = res.data
      ElMessage.success('查询成功')
    } else {
      ElMessage.error(res.msg || '查询失败')
      currentLevel.value = null
    }
  } catch (error) {
    ElMessage.error('查询失败')
  } finally {
    querying.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true

    const res = await changeLevel({
      user_id: form.user_id,
      level: form.level
    })

    if (res.code === '0') {
      ElMessage.success(res.msg || '修改成功')

      // 显示结果
      resultData.value = res.data

      // 自动查询新的等级信息
      setTimeout(() => {
        handleQuery()
      }, 500)
    } else {
      ElMessage.error(res.msg || '修改失败')
      resultData.value = null
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    submitting.value = false
  }
}

// 重置表单
const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  currentLevel.value = null
  resultData.value = null
}
</script>

<style scoped>
.change-level {
  padding: 0;
}

.form-card {
  margin-bottom: 20px;
}

.current-level-card {
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
</style>

<template>
  <div class="order-manage">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span><strong>订单管理</strong>添加用户订单</span>
          <el-tag type="info">测试环境</el-tag>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="140px">
        <el-form-item label="学员ID" prop="stu_id">
          <HistoryInput
            v-model="form.stu_id"
            placeholder="请输入学员ID"
            clearable
            storage-key="order-manage_stu_id"
            style="width: 300px">
            <template #prepend>
              <el-icon><User /></el-icon>
            </template>
          </HistoryInput>
        </el-form-item>

        <el-form-item label="订单金额" prop="order_money">
          <el-input-number v-model="form.order_money" :min="1" :step="100" />
        </el-form-item>

        <el-form-item label="优惠金额" prop="discount_money">
          <el-input-number v-model="form.discount_money" :min="0" :step="10" />
        </el-form-item>

        <el-form-item label="显示金额" prop="display_money">
          <el-input-number v-model="form.display_money" :min="1" :step="100" />
        </el-form-item>

        <el-form-item label="商品ID" prop="goods_id">
          <HistoryInput
            v-model="form.goods_id"
            placeholder="请输入商品ID"
            clearable
            storage-key="order-manage_goods_id"
            style="width: 300px">
          </HistoryInput>
        </el-form-item>

        <el-form-item label="订单类型" prop="order_type">
          <el-select v-model="form.order_type" placeholder="请选择订单类型" style="width: 300px">
            <el-option label="point_package" value="point_package" />
            <el-option label="course_package" value="course_package" />
          </el-select>
        </el-form-item>

        <el-form-item label="支付方式" prop="pay_method">
          <el-select v-model="form.pay_method" placeholder="请选择支付方式" style="width: 300px">
            <el-option label="Bank" value="Bank" />
            <el-option label="Alipay" value="Alipay" />
            <el-option label="WeChat" value="WeChat" />
          </el-select>
        </el-form-item>

        <el-form-item label="银行" prop="bank">
          <el-select v-model="form.bank" placeholder="请选择银行" style="width: 300px">
            <el-option label="中国银行" value="zh" />
            <el-option label="工商银行" value="gs" />
            <el-option label="建设银行" value="js" />
          </el-select>
        </el-form-item>

        <el-form-item label="订单状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择订单状态" style="width: 300px">
            <el-option label="开启" value="on" />
            <el-option label="关闭" value="off" />
          </el-select>
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <HistoryInput
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
            clearable
            storage-key="order-manage_remark">
          </HistoryInput>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            添加订单
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 结果展示 -->
    <el-card v-if="result" class="result-card">
      <template #header>
        <div class="card-header">
          <span>操作结果</span>
          <el-tag :type="result.success ? 'success' : 'danger'">
            {{ result.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <div v-if="result.success" class="success-result">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="学员ID">{{ result.stu_id }}</el-descriptions-item>
          <el-descriptions-item label="订单ID">{{ result.order_id }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ result.order_money }}</el-descriptions-item>
          <el-descriptions-item label="优惠金额">¥{{ result.discount_money }}</el-descriptions-item>
          <el-descriptions-item label="实际支付">¥{{ result.actual_money }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <el-alert
        v-else
        :title="result.message || '操作失败'"
        type="error"
        :closable="false"
        show-icon />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { addOrder } from '@/api/order'

const formRef = ref(null)

const form = reactive({
  stu_id: '',
  order_money: 1599,
  discount_money: 100,
  display_money: 5299,
  goods_id: '263147',
  order_type: 'point_package',
  pay_method: 'Bank',
  bank: 'zh',
  status: 'on',
  remark: ''
})

const rules = {
  stu_id: [
    { required: true, message: '请输入学员ID', trigger: 'blur' },
    { pattern: /^\d+$/, message: '学员ID必须是数字', trigger: 'blur' }
  ],
  order_money: [
    { required: true, message: '请输入订单金额', trigger: 'blur' }
  ],
  goods_id: [
    { required: true, message: '请输入商品ID', trigger: 'blur' }
  ],
  order_type: [
    { required: true, message: '请选择订单类型', trigger: 'change' }
  ],
  pay_method: [
    { required: true, message: '请选择支付方式', trigger: 'change' }
  ]
}

const loading = ref(false)
const result = ref(null)

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    loading.value = true
    result.value = null

    const res = await addOrder({
      stu_id: form.stu_id,
      order_money: form.order_money,
      discount_money: form.discount_money,
      display_money: form.display_money,
      goods_id: form.goods_id,
      order_type: form.order_type,
      pay_method: form.pay_method,
      bank: form.bank,
      status: form.status,
      remark: form.remark
    })

    if (res.code === '0') {
      result.value = {
        success: true,
        stu_id: form.stu_id,
        order_id: res.data?.order_id,
        order_money: form.order_money,
        discount_money: form.discount_money,
        actual_money: form.order_money - form.discount_money
      }
      ElMessage.success('订单添加成功')
    } else {
      result.value = {
        success: false,
        message: res.msg || '订单添加失败'
      }
      ElMessage.error(res.msg || '订单添加失败')
    }
  } catch (error) {
    if (error !== false) {
      ElMessage.error('表单验证失败')
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  result.value = null
}
</script>

<style scoped>
.order-manage {
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

.success-result {
  padding: 10px 0;
}
</style>

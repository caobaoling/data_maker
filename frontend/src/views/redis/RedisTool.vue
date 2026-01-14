<template>
  <div class="redis-tool">
    <!-- 顶部节点选择栏 -->
    <el-card class="header-card">
      <div class="node-selection">
        <div class="node-title">Redis节点选择：</div>
        <el-checkbox-group v-model="selectedNodeIndexes" @change="handleNodeSelectionChange">
          <el-checkbox
            v-for="(node, index) in redisNodes"
            :key="index"
            :label="index"
            border
            style="margin-right: 15px">
            <el-icon><Connection /></el-icon>
            <span style="margin-left: 5px">{{ node.name }}</span>
            <span style="color: #909399; font-size: 12px; margin-left: 5px">
              ({{ node.host }}:{{ node.port }})
            </span>
          </el-checkbox>
        </el-checkbox-group>
      </div>
    </el-card>

    <!-- 搜索区域 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="模糊搜索">
          <el-input
            v-model="searchForm.keyword"
            placeholder="输入关键词，如: 58153803, appoint"
            style="width: 400px"
            clearable
            @keyup.enter="handleSearch">
            <template #prepend>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button type="primary" :loading="searching" @click="handleSearch">
                搜索
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button :icon="Delete" :disabled="selectedKeys.length === 0" @click="handleBatchDelete">
            批量删除 ({{ selectedKeys.length }})
          </el-button>
        </el-form-item>
      </el-form>
      <div v-if="searchForm.keyword" class="search-tip">
        <el-tag type="info" size="small">
          搜索模式: *{{ searchForm.keyword }}*
        </el-tag>
        <span style="margin-left: 10px; color: #909399; font-size: 12px">
          将在 {{ selectedNodeIndexes.length }} 个节点中查找包含 "{{ searchForm.keyword }}" 的键
        </span>
      </div>
    </el-card>

    <!-- 键列表 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>键列表 (共 {{ keyList.length }} 个)</span>
          <div>
            <el-button text @click="handleSelectAll">全选</el-button>
            <el-button text @click="handleClearSelection">清除选择</el-button>
          </div>
        </div>
      </template>

      <el-table
        ref="tableRef"
        :data="paginatedKeys"
        stripe
        border
        @selection-change="handleSelectionChange"
        v-loading="searching"
        max-height="500">
        <el-table-column type="selection" width="55" />
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="key" label="键名" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleViewDetail(row.key)">{{ row.key }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="node" label="所在节点" width="150">
          <template #default="{ row }">
            <el-tag size="small" type="success">{{ row.nodeName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template #default="{ row }">
            <el-button type="primary" text :icon="View" @click="handleViewDetail(row.key, row.nodeIndex)">
              查看
            </el-button>
            <el-button type="danger" text :icon="Delete" @click="handleSingleDelete(row.key, row.nodeIndex)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-if="keyList.length > 0"
        class="pagination"
        v-model:current-page="pagination.current"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[50, 100, 200, 500]"
        :total="keyList.length"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>

    <!-- 多节点删除预览对话框 -->
    <el-dialog
      v-model="multiNodeDialog.visible"
      title="多节点删除预览"
      width="70%"
      :close-on-click-modal="false">
      <!-- 第一步：选择节点 -->
      <div v-if="multiNodeDialog.step === 1">
        <el-alert type="info" :closable="false" style="margin-bottom: 20px">
          <template #title>
            <strong>第一步：选择要操作的Redis节点</strong>
          </template>
          请选择要执行删除操作的Redis节点。系统将在选中的所有节点上执行相同的匹配模式删除。
        </el-alert>

        <el-form :model="multiNodeDialog" label-width="100px">
          <el-form-item label="匹配模式">
            <el-tag type="danger" size="large">{{ multiNodeDialog.pattern }}</el-tag>
          </el-form-item>

          <el-form-item label="选择节点">
            <el-checkbox-group v-model="multiNodeDialog.selectedNodes">
              <el-checkbox
                v-for="node in redisNodes"
                :key="`${node.host}:${node.port}`"
                :label="node"
                border
                style="margin: 5px">
                <el-tag type="success">{{ node.name }}</el-tag>
                <span style="margin-left: 10px">{{ node.host }}:{{ node.port }}</span>
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item>
            <el-button @click="handleSelectAllNodes">全选</el-button>
            <el-button @click="multiNodeDialog.selectedNodes = []">清空</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 第二步：预览结果 -->
      <div v-else-if="multiNodeDialog.step === 2">
        <el-alert type="warning" :closable="false" style="margin-bottom: 20px">
          <template #title>
            <strong>⚠️ 多节点删除警告</strong>
          </template>
          即将在 <el-tag type="warning">{{ multiNodeDialog.selectedNodes.length }} 个节点</el-tag> 上删除匹配模式
          <el-tag type="danger">{{ multiNodeDialog.pattern }}</el-tag> 的所有键！<br>
          总共找到 <el-tag type="danger">{{ multiNodeDialog.totalCount }} 个键</el-tag>，
          此操作<strong>不可恢复</strong>。
        </el-alert>

        <el-divider content-position="left">各节点统计</el-divider>

        <el-table
          :data="multiNodeDialog.nodeResults"
          stripe
          border
          max-height="300">
          <el-table-column prop="node" label="节点" width="150" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag v-if="row.success" type="success">成功</el-tag>
              <el-tag v-else type="danger">失败</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="匹配键数" width="120" />
          <el-table-column prop="error" label="错误信息" show-overflow-tooltip />
        </el-table>

        <el-divider content-position="left">预览键列表（前100个）</el-divider>

        <el-table
          :data="multiNodeDialog.previewKeys"
          stripe
          border
          max-height="300"
          v-loading="multiNodeDialog.loading">
          <el-table-column type="index" label="序号" width="80" />
          <el-table-column prop="key" label="键名" show-overflow-tooltip>
            <template #default="{ row }">
              {{ row }}
            </template>
          </el-table-column>
        </el-table>
      </div>

      <template #footer>
        <div v-if="multiNodeDialog.step === 1">
          <el-button @click="multiNodeDialog.visible = false">取消</el-button>
          <el-button
            type="primary"
            :disabled="multiNodeDialog.selectedNodes.length === 0"
            :loading="multiNodeDialog.loading"
            @click="handlePreviewMultiNode">
            下一步：预览 ({{ multiNodeDialog.selectedNodes.length }} 个节点)
          </el-button>
        </div>
        <div v-else-if="multiNodeDialog.step === 2">
          <el-button @click="multiNodeDialog.step = 1">上一步</el-button>
          <el-button @click="multiNodeDialog.visible = false">取消</el-button>
          <el-button
            type="danger"
            :loading="multiNodeDialog.deleting"
            @click="handleConfirmMultiNodeDelete">
            确认删除 {{ multiNodeDialog.totalCount }} 个键
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 删除预览对话框 -->
    <el-dialog
      v-model="previewDialog.visible"
      title="删除预览"
      width="60%"
      :close-on-click-modal="false">
      <el-alert type="warning" :closable="false" style="margin-bottom: 20px">
        <template #title>
          <strong>⚠️ 危险操作警告</strong>
        </template>
        即将删除匹配模式 <el-tag type="danger">{{ previewDialog.pattern }}</el-tag> 的所有键！<br>
        此操作<strong>不可恢复</strong>，请仔细检查下方预览的键列表。
      </el-alert>

      <el-descriptions :column="2" border style="margin-bottom: 20px">
        <el-descriptions-item label="匹配模式">
          <el-tag type="danger">{{ previewDialog.pattern }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="匹配总数">
          <el-tag type="warning">{{ previewDialog.count }} 个键</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="预览显示">
          前 {{ previewDialog.previewCount }} 个
        </el-descriptions-item>
        <el-descriptions-item label="更多键">
          <el-tag v-if="previewDialog.hasMore" type="info">还有更多键未显示...</el-tag>
          <el-tag v-else type="success">已显示全部</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left">预览键列表</el-divider>

      <el-table
        :data="previewDialog.keys"
        stripe
        border
        max-height="400"
        v-loading="previewDialog.loading">
        <el-table-column type="index" label="序号" width="80" />
        <el-table-column prop="key" label="键名" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row }}
          </template>
        </el-table-column>
      </el-table>

      <template #footer>
        <el-button @click="handleCancelPreview">取消</el-button>
        <el-button
          type="danger"
          :loading="previewDialog.deleting"
          @click="handleConfirmDelete">
          确认删除 {{ previewDialog.count }} 个键
        </el-button>
      </template>
    </el-dialog>

    <!-- 键详情抽屉 -->
    <el-drawer
      v-model="detailDrawer.visible"
      title="键详情"
      size="50%"
      :before-close="handleCloseDetail">
      <div v-if="detailDrawer.data" class="key-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="键名">
            <el-tag type="primary">{{ detailDrawer.data.key }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="类型">
            <el-tag :type="getTypeColor(detailDrawer.data.type)">
              {{ detailDrawer.data.type.toUpperCase() }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="TTL">
            <el-tag v-if="detailDrawer.data.ttl === -1" type="success">永久</el-tag>
            <el-tag v-else-if="detailDrawer.data.ttl === -2" type="danger">已过期</el-tag>
            <el-tag v-else type="warning">{{ detailDrawer.data.ttl }}秒</el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider content-position="left">键值内容</el-divider>

        <!-- String类型 -->
        <div v-if="detailDrawer.data.type === 'string'" class="value-display">
          <el-input
            v-model="detailDrawer.data.value"
            type="textarea"
            :rows="10"
            readonly
          />
        </div>

        <!-- Hash类型 -->
        <div v-else-if="detailDrawer.data.type === 'hash'" class="value-display">
          <el-table :data="formatHashData(detailDrawer.data.value)" border stripe max-height="400">
            <el-table-column prop="key" label="字段" width="200" />
            <el-table-column prop="value" label="值" show-overflow-tooltip />
          </el-table>
        </div>

        <!-- List类型 -->
        <div v-else-if="detailDrawer.data.type === 'list'" class="value-display">
          <el-table :data="formatListData(detailDrawer.data.value)" border stripe max-height="400">
            <el-table-column type="index" label="索引" width="80" />
            <el-table-column prop="value" label="值" show-overflow-tooltip />
          </el-table>
        </div>

        <!-- Set类型 -->
        <div v-else-if="detailDrawer.data.type === 'set'" class="value-display">
          <el-table :data="formatListData(detailDrawer.data.value)" border stripe max-height="400">
            <el-table-column type="index" label="序号" width="80" />
            <el-table-column prop="value" label="成员" show-overflow-tooltip />
          </el-table>
        </div>

        <!-- ZSet类型 -->
        <div v-else-if="detailDrawer.data.type === 'zset'" class="value-display">
          <el-table :data="detailDrawer.data.value" border stripe max-height="400">
            <el-table-column prop="member" label="成员" show-overflow-tooltip />
            <el-table-column prop="score" label="分数" width="120" />
          </el-table>
        </div>

        <!-- 其他类型 -->
        <div v-else class="value-display">
          <el-alert type="info" :closable="false">
            {{ detailDrawer.data.value_str }}
          </el-alert>
        </div>
      </div>

      <template #footer>
        <el-button @click="handleCloseDetail">关闭</el-button>
        <el-button type="danger" :icon="Delete" @click="handleDeleteFromDetail">
          删除此键
        </el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Connection, Search, Delete, Refresh, View } from '@element-plus/icons-vue'
import {
  getRedisConfig,
  searchRedisKeys,
  getKeyInfo,
  deleteKeys,
  deleteByPattern,
  getRedisStats,
  multiNodeDeleteByPattern
} from '@/api/redis'

// Redis配置
const redisConfig = ref({
  host: '172.16.70.21',
  port: 6379,
  password: null
})

// Redis节点列表
const redisNodes = ref([])

// 选中的节点索引列表（多选）
const selectedNodeIndexes = ref([0])  // 默认选中第一个节点

// 每个节点的统计信息
const nodeStats = ref([
  { db_size: 0, used_memory: 'N/A', active: true },
  { db_size: 0, used_memory: 'N/A', active: false },
  { db_size: 0, used_memory: 'N/A', active: false }
])

// 当前节点配置（用于向后兼容）
const currentNode = computed(() => {
  if (redisNodes.value.length > 0 && selectedNodeIndexes.value.length > 0) {
    return redisNodes.value[selectedNodeIndexes.value[0]]
  }
  return redisConfig.value
})

// 统计信息（保留用于兼容）
const stats = reactive({
  db_size: 0,
  used_memory: 'N/A',
  connected_clients: 0,
  redis_version: 'N/A'
})

// 搜索表单
const searchForm = reactive({
  keyword: ''  // 关键词搜索，自动转换为 *keyword*
})

// 键列表（包含节点信息）
const keyList = ref([])
const selectedKeys = ref([])
const searching = ref(false)

// 表格引用
const tableRef = ref(null)

// 分页
const pagination = reactive({
  current: 1,
  pageSize: 100
})

// 计算分页后的数据
const paginatedKeys = computed(() => {
  const start = (pagination.current - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return keyList.value.slice(start, end)
})

// 键详情抽屉
const detailDrawer = reactive({
  visible: false,
  data: null
})

// 删除预览对话框
const previewDialog = reactive({
  visible: false,
  pattern: '',
  count: 0,
  keys: [],
  previewCount: 0,
  hasMore: false,
  loading: false,
  deleting: false
})

// 多节点删除对话框
const multiNodeDialog = reactive({
  visible: false,
  step: 1, // 1: 选择节点, 2: 预览结果
  pattern: '',
  selectedNodes: [],
  totalCount: 0,
  nodeResults: [],
  previewKeys: [],
  loading: false,
  deleting: false
})

// 加载Redis配置
const loadConfig = async () => {
  try {
    const res = await getRedisConfig()
    if (res.code === '0') {
      redisConfig.value = res.data.default
      redisNodes.value = res.data.nodes || []

      // 默认选中第一个节点
      if (redisNodes.value.length > 0) {
        selectedNodeIndexes.value = [0]
      }

      // 加载所有节点统计
      loadAllStats()
    }
  } catch (error) {
    console.error('加载配置失败:', error)
  }
}

// 节点选择变化
const handleNodeSelectionChange = (indexes) => {
  // 至少保留一个节点
  if (indexes.length === 0) {
    ElMessage.warning('至少需要选择一个节点')
    selectedNodeIndexes.value = [0]
    return
  }

  // 更新节点激活状态
  nodeStats.value.forEach((stat, index) => {
    stat.active = indexes.includes(index)
  })

  loadAllStats()
}

// 加载所有节点统计信息
const loadAllStats = async () => {
  for (let i = 0; i < redisNodes.value.length; i++) {
    const node = redisNodes.value[i]
    try {
      const res = await getRedisStats({ redis_config: node })
      if (res.code === '0') {
        nodeStats.value[i] = {
          ...res.data,
          active: selectedNodeIndexes.value.includes(i)
        }
      }
    } catch (error) {
      console.error(`获取节点 ${node.name} 统计失败:`, error)
    }
  }
}

// 加载统计信息（兼容旧代码）
const loadStats = async () => {
  loadAllStats()
}

// 搜索键（支持多节点）
const handleSearch = async () => {
  if (!searchForm.keyword) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  searching.value = true
  keyList.value = []
  selectedKeys.value = []

  try {
    // 构建模糊搜索模式
    const pattern = `*${searchForm.keyword}*`

    // 在所有选中的节点上搜索
    const searchPromises = selectedNodeIndexes.value.map(async (nodeIndex) => {
      const node = redisNodes.value[nodeIndex]
      try {
        const res = await searchRedisKeys({
          pattern: pattern,
          redis_config: node
        })

        if (res.code === '0' && res.data.keys) {
          // 为每个键添加节点信息
          return res.data.keys.map(key => ({
            key: key,
            nodeIndex: nodeIndex,
            nodeName: node.name,
            nodeConfig: node
          }))
        }
        return []
      } catch (error) {
        console.error(`节点 ${node.name} 搜索失败:`, error)
        return []
      }
    })

    // 等待所有节点搜索完成
    const results = await Promise.all(searchPromises)

    // 合并所有节点的结果
    keyList.value = results.flat()
    pagination.current = 1

    ElMessage.success(`在 ${selectedNodeIndexes.value.length} 个节点中找到 ${keyList.value.length} 个匹配的键`)

    // 刷新统计
    loadAllStats()
  } catch (error) {
    ElMessage.error('搜索失败')
  } finally {
    searching.value = false
  }
}

// 处理选择变化
const handleSelectionChange = (selection) => {
  selectedKeys.value = selection
}

// 全选
const handleSelectAll = () => {
  if (tableRef.value) {
    tableRef.value.toggleAllSelection()
  }
}

// 清除选择
const handleClearSelection = () => {
  selectedKeys.value = []
  if (tableRef.value) {
    tableRef.value.clearSelection()
  }
}

// 查看键详情
const handleViewDetail = async (key, nodeIndex) => {
  try {
    // 如果没有传nodeIndex，从keyList中查找
    if (nodeIndex === undefined) {
      const keyItem = keyList.value.find(item => item.key === key)
      if (keyItem) {
        nodeIndex = keyItem.nodeIndex
      }
    }

    const nodeConfig = redisNodes.value[nodeIndex] || currentNode.value
    const res = await getKeyInfo({
      key: key,
      redis_config: nodeConfig
    })

    if (res.code === '0') {
      detailDrawer.data = res.data
      detailDrawer.visible = true
    } else {
      ElMessage.error(res.msg || '获取键信息失败')
    }
  } catch (error) {
    ElMessage.error('获取键信息失败')
  }
}

// 单个删除
const handleSingleDelete = async (key, nodeIndex) => {
  try {
    await ElMessageBox.confirm(`确定要删除键 "${key}" 吗？`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    // 如果没有传nodeIndex，从keyList中查找
    if (nodeIndex === undefined) {
      const keyItem = keyList.value.find(item => item.key === key)
      if (keyItem) {
        nodeIndex = keyItem.nodeIndex
      }
    }

    const nodeConfig = redisNodes.value[nodeIndex] || currentNode.value
    const res = await deleteKeys({
      keys: [key],
      redis_config: nodeConfig
    })

    if (res.code === '0') {
      ElMessage.success('删除成功')
      // 从列表中移除
      keyList.value = keyList.value.filter(item => item.key !== key)
      loadAllStats()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (selectedKeys.value.length === 0) {
    ElMessage.warning('请先选择要删除的键')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedKeys.value.length} 个键吗？`,
      '批量删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 按节点分组删除
    const deletePromises = []
    const keysByNode = {}

    // 将选中的键按节点分组
    selectedKeys.value.forEach(item => {
      const nodeIndex = item.nodeIndex
      if (!keysByNode[nodeIndex]) {
        keysByNode[nodeIndex] = []
      }
      keysByNode[nodeIndex].push(item.key)
    })

    // 对每个节点执行删除
    for (const [nodeIndex, keys] of Object.entries(keysByNode)) {
      const node = redisNodes.value[parseInt(nodeIndex)]
      deletePromises.push(
        deleteKeys({
          keys: keys,
          redis_config: node
        })
      )
    }

    // 等待所有删除完成
    const results = await Promise.all(deletePromises)

    let totalDeleted = 0
    results.forEach(res => {
      if (res.code === '0') {
        totalDeleted += res.data.deleted_count
      }
    })

    ElMessage.success(`成功删除 ${totalDeleted} 个键`)

    // 从列表中移除已删除的键
    const deletedKeys = selectedKeys.value.map(item => item.key)
    keyList.value = keyList.value.filter(item => !deletedKeys.includes(item.key))
    selectedKeys.value = []

    loadAllStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 按模式删除 - 第一步：预览
const handleDeleteByPattern = async () => {
  if (!searchForm.pattern) {
    ElMessage.warning('请输入要删除的模式')
    return
  }

  // 重置预览对话框
  previewDialog.pattern = searchForm.pattern
  previewDialog.visible = true
  previewDialog.loading = true
  previewDialog.keys = []
  previewDialog.count = 0

  try {
    const nodeConfig = currentNode.value
    // 第一步：调用dry_run=true预览
    const res = await deleteByPattern({
      pattern: searchForm.pattern,
      redis_config: nodeConfig,
      dry_run: true  // 预览模式
    })

    if (res.code === '0') {
      previewDialog.count = res.data.count
      previewDialog.keys = res.data.keys
      previewDialog.previewCount = res.data.preview_count
      previewDialog.hasMore = res.data.has_more
    } else {
      ElMessage.error(res.msg || '预览失败')
      previewDialog.visible = false
    }
  } catch (error) {
    ElMessage.error('预览失败')
    previewDialog.visible = false
  } finally {
    previewDialog.loading = false
  }
}

// 按模式删除 - 第二步：确认删除
const handleConfirmDelete = async () => {
  previewDialog.deleting = true

  try {
    const nodeConfig = currentNode.value
    // 第二步：调用dry_run=false真正删除
    const res = await deleteByPattern({
      pattern: previewDialog.pattern,
      redis_config: nodeConfig,
      dry_run: false  // 实际删除
    })

    if (res.code === '0') {
      ElMessage.success(`成功删除 ${res.data.deleted_count} 个键`)
      // 关闭对话框
      previewDialog.visible = false
      // 清空列表
      keyList.value = []
      selectedKeys.value = []
      // 刷新统计
      loadStats()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    previewDialog.deleting = false
  }
}

// 取消预览
const handleCancelPreview = () => {
  previewDialog.visible = false
}

// 多节点删除 - 第一步：打开对话框
const handleMultiNodeDelete = () => {
  if (!searchForm.pattern) {
    ElMessage.warning('请先输入要删除的模式')
    return
  }

  // 重置对话框
  multiNodeDialog.pattern = searchForm.pattern
  multiNodeDialog.step = 1
  multiNodeDialog.selectedNodes = []
  multiNodeDialog.visible = true
}

// 全选节点
const handleSelectAllNodes = () => {
  multiNodeDialog.selectedNodes = [...redisNodes.value]
}

// 多节点删除 - 第二步：预览
const handlePreviewMultiNode = async () => {
  if (multiNodeDialog.selectedNodes.length === 0) {
    ElMessage.warning('请至少选择一个节点')
    return
  }

  multiNodeDialog.loading = true

  try {
    // 调用多节点预览API
    const res = await multiNodeDeleteByPattern({
      pattern: multiNodeDialog.pattern,
      nodes: multiNodeDialog.selectedNodes,
      dry_run: true  // 预览模式
    })

    if (res.code === '0') {
      multiNodeDialog.totalCount = res.data.total_count
      multiNodeDialog.nodeResults = res.data.node_results
      multiNodeDialog.previewKeys = res.data.preview_keys || []
      multiNodeDialog.step = 2  // 进入第二步
    } else {
      ElMessage.error(res.msg || '预览失败')
    }
  } catch (error) {
    ElMessage.error('预览失败')
  } finally {
    multiNodeDialog.loading = false
  }
}

// 多节点删除 - 第三步：确认删除
const handleConfirmMultiNodeDelete = async () => {
  multiNodeDialog.deleting = true

  try {
    // 调用多节点删除API
    const res = await multiNodeDeleteByPattern({
      pattern: multiNodeDialog.pattern,
      nodes: multiNodeDialog.selectedNodes,
      dry_run: false  // 实际删除
    })

    if (res.code === '0') {
      ElMessage.success(`成功删除 ${res.data.total_deleted} 个键`)

      // 显示每个节点的删除结果
      const results = res.data.node_results
      const successNodes = results.filter(r => r.success).length
      const failedNodes = results.filter(r => !r.success).length

      if (failedNodes > 0) {
        ElMessage.warning(`${successNodes} 个节点成功，${failedNodes} 个节点失败`)
      }

      // 关闭对话框
      multiNodeDialog.visible = false
      // 清空列表
      keyList.value = []
      selectedKeys.value = []
      // 刷新统计
      loadStats()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    multiNodeDialog.deleting = false
  }
}

// 从详情页删除
const handleDeleteFromDetail = async () => {
  if (!detailDrawer.data) return

  try {
    await ElMessageBox.confirm(`确定要删除键 "${detailDrawer.data.key}" 吗？`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const nodeConfig = currentNode.value
    const res = await deleteKeys({
      keys: [detailDrawer.data.key],
      redis_config: nodeConfig
    })

    if (res.code === '0') {
      ElMessage.success('删除成功')
      // 从列表中移除
      keyList.value = keyList.value.filter(k => k !== detailDrawer.data.key)
      detailDrawer.visible = false
      loadStats()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 关闭详情
const handleCloseDetail = () => {
  detailDrawer.visible = false
  detailDrawer.data = null
}

// 分页处理
const handleSizeChange = () => {
  pagination.current = 1
}

const handleCurrentChange = () => {
  // 分页变化时不需要额外操作
}

// 格式化Hash数据
const formatHashData = (hashObj) => {
  if (!hashObj) return []
  return Object.entries(hashObj).map(([key, value]) => ({ key, value }))
}

// 格式化List/Set数据
const formatListData = (arr) => {
  if (!arr) return []
  return arr.map(value => ({ value }))
}

// 获取类型颜色
const getTypeColor = (type) => {
  const colorMap = {
    string: 'success',
    hash: 'warning',
    list: 'primary',
    set: 'info',
    zset: 'danger'
  }
  return colorMap[type] || 'default'
}

// 初始化
onMounted(() => {
  loadConfig()
  loadStats()
})
</script>

<style scoped>
.redis-tool {
  padding: 0;
}

.node-selection {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
}

.node-title {
  font-weight: 500;
  color: #303133;
  min-width: 120px;
}

.search-tip {
  margin-top: 10px;
  padding: 8px 12px;
  background: #f4f4f5;
  border-radius: 4px;
}

.header-card {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.config-info {
  display: flex;
  align-items: center;
}

.stats-info {
  display: flex;
  gap: 40px;
  flex: 1;
  justify-content: center;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.key-detail {
  padding: 20px;
}

.value-display {
  margin-top: 20px;
}
</style>

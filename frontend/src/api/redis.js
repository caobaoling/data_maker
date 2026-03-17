import request from './request'

// 获取默认Redis配置
export function getRedisConfig() {
  return request({
    url: '/api/redis/config',
    method: 'get'
  })
}

// 搜索Redis键
export function searchRedisKeys(data) {
  return request({
    url: '/api/redis/search',
    method: 'post',
    data
  })
}

// 获取键详细信息
export function getKeyInfo(data) {
  return request({
    url: '/api/redis/key/info',
    method: 'post',
    data
  })
}

// 删除Redis键（批量）
export function deleteKeys(data) {
  return request({
    url: '/api/redis/key/delete',
    method: 'post',
    data
  })
}

// 按模式删除Redis键（支持预览模式）
// data: { pattern, redis_config, dry_run }
// dry_run=true: 预览模式，只查询不删除
// dry_run=false: 实际删除
export function deleteByPattern(data) {
  return request({
    url: '/api/redis/key/delete_by_pattern',
    method: 'post',
    data
  })
}

// 获取Redis统计信息
export function getRedisStats(data) {
  return request({
    url: '/api/redis/stats',
    method: 'post',
    data
  })
}

// 测试Redis连接
export function pingRedis(data) {
  return request({
    url: '/api/redis/ping',
    method: 'post',
    data
  })
}

// 多节点按模式删除Redis键（支持预览模式）
// data: { pattern, nodes, dry_run }
// nodes: [{ host, port, name }, ...]
// dry_run=true: 预览模式，只查询不删除
// dry_run=false: 实际删除
export function multiNodeDeleteByPattern(data) {
  return request({
    url: '/api/redis/multi_node/delete_by_pattern',
    method: 'post',
    data
  })
}

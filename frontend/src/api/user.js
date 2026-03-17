import request from './request'

/**
 * 添加用户财富
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.sku_type - 财富类型
 * @param {number} data.count - 数量
 * @param {number} data.days - 有效天数
 */
export function addWealth(data) {
  return request({
    url: '/api/user/add_wealth',
    method: 'post',
    data
  })
}

/**
 * 查询用户财富
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.sku_type - 财富类型（可选）
 */
export function queryWealth(data) {
  return request({
    url: '/api/user/query_wealth',
    method: 'post',
    data
  })
}

/**
 * 获取所有财富类型
 */
export function getWealthTypes() {
  return request({
    url: '/api/user/wealth_types',
    method: 'get'
  })
}

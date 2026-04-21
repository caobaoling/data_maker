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

/**
 * 获取阿语标签类型列表
 */
export function getArabicTagTypes() {
  return request({
    url: '/api/user/arabic_tag_types',
    method: 'get'
  })
}

/**
 * 查询用户阿语标签
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.type - 标签类型（ar_tea/ar_point）
 */
export function queryArabicTag(data) {
  return request({
    url: '/api/user/arabic_tag/query',
    method: 'post',
    data
  })
}

/**
 * 为用户添加阿语标签
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.type - 标签类型（ar_tea/ar_point）
 */
export function addArabicTag(data) {
  return request({
    url: '/api/user/arabic_tag/add',
    method: 'post',
    data
  })
}

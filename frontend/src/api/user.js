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

/**
 * 通过用户ID获取手机号
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.region - 区域（domestic/overseas）
 */
export function getMobile(data) {
  return request({
    url: '/api/user/get_mobile',
    method: 'post',
    data
  })
}

/**
 * 为用户打海外标签
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.country_code - 国家代码
 */
export function addOverseasLabel(data) {
  return request({
    url: '/api/user/add_overseas_label',
    method: 'post',
    data
  })
}

/**
 * 查询用户海外标签
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 */
export function queryOverseasLabel(data) {
  return request({
    url: '/api/user/query_overseas_label',
    method: 'post',
    data
  })
}

/**
 * 删除用户海外标签
 * @param {Object} data - 请求参数
 * @param {string} data.user_id - 用户ID
 * @param {string} data.country_code - 国家代码
 */
export function deleteOverseasLabel(data) {
  return request({
    url: '/api/user/delete_overseas_label',
    method: 'post',
    data
  })
}

/**
 * 查询用户Cocos标签
 */
export function queryCocosLabel(data) {
  return request({ url: '/api/user/query_cocos_label', method: 'post', data })
}

/**
 * 添加用户Cocos标签
 */
export function addCocosLabel(data) {
  return request({ url: '/api/user/add_cocos_label', method: 'post', data })
}

/**
 * 删除用户Cocos标签
 */
export function deleteCocosLabel(data) {
  return request({ url: '/api/user/delete_cocos_label', method: 'post', data })
}

/**
 * 通过手机号解锁账户
 * @param {Object} data - 请求参数
 * @param {string} data.username - 手机号
 * @param {string} data.region - 区域（domestic/overseas）
 */
export function unlockAccount(data) {
  return request({
    url: '/api/user/unlock_account',
    method: 'post',
    data
  })
}

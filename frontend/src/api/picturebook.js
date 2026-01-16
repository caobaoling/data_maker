// 文件: api/picturebook.js
// 作者: Claude Code
// 创建日期: 2026/01/16
// 描述: 绘本系统API接口

import request from './request'

/**
 * 清除用户绘本学习计划
 * @param {Object} params - 参数对象
 * @param {string|number} params.user_id - 用户ID
 * @returns {Promise} API响应
 */
export function clearPicturebookPlan(params) {
  return request({
    url: '/picturebook/clear_plan',
    method: 'post',
    data: params
  })
}

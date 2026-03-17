import request from './request'

// 添加AI点数
export function addPoint(data) {
  return request({
    url: '/api/ai/add_point',
    method: 'post',
    data
  })
}

// 查询AI点数
export function queryPoint(data) {
  return request({
    url: '/api/ai/query_point',
    method: 'post',
    data
  })
}

// 使用兑换码
export function useExchangeCode(data) {
  return request({
    url: '/api/ai/use_exchange_code',
    method: 'post',
    data
  })
}

// 清空学习计划
export function clearStudyPlan(data) {
  return request({
    url: '/api/ai/clear_study_plan',
    method: 'post',
    data
  })
}

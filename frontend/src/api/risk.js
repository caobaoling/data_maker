import request from './request'

// 解除高风险
export function releaseRisk(data) {
  return request({
    url: '/api/risk/release',
    method: 'post',
    data
  })
}

// 添加白名单
export function addWhitelist(data) {
  return request({
    url: '/api/risk/whitelist',
    method: 'post',
    data
  })
}

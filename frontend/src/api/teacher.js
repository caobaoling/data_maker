import request from './request'

// 添加合同
export function addContract(data) {
  return request({
    url: '/api/teacher/add_contract',
    method: 'post',
    data
  })
}

// 查询合同
export function queryContract(data) {
  return request({
    url: '/api/teacher/query_contract',
    method: 'post',
    data
  })
}
